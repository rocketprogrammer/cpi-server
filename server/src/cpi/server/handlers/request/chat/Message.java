package cpi.server.handlers.request.chat;

import com.smartfoxserver.v2.entities.Room;
import com.smartfoxserver.v2.entities.data.ISFSObject;
import com.smartfoxserver.v2.entities.data.SFSObject;
import com.smartfoxserver.v2.extensions.BaseClientRequestHandler;
import com.smartfoxserver.v2.entities.User;
import org.bouncycastle.jce.provider.BouncyCastleProvider;

import javax.crypto.BadPaddingException;
import javax.crypto.Cipher;
import javax.crypto.IllegalBlockSizeException;
import javax.crypto.NoSuchPaddingException;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.SecretKeySpec;
import java.nio.charset.StandardCharsets;
import java.security.*;
import java.security.spec.AlgorithmParameterSpec;
import java.security.spec.InvalidKeySpecException;
import java.util.Base64;

public class Message extends BaseClientRequestHandler {
    @Override
    public void handleClientRequest(User user, ISFSObject params) {
        trace("CHAT_MESSAGE + ", params.getDump());

        String msg = params.getUtfString("msg");
        byte[] message = Base64.getDecoder().decode(msg);
        String aesKey = "dZJrQkW32sXkeVF9G3Zc0jeO7UzCUEhs";

        ISFSObject data = new SFSObject();

        // Required for AES PKCS7 decryption.
        Security.addProvider(new BouncyCastleProvider());

        try {
            Cipher cipher = Cipher.getInstance("AES/CBC/PKCS7Padding");
            byte[] key = aesKey.getBytes();

            SecretKeySpec keySpec = new SecretKeySpec(key, "AES");
            byte[] iv = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
            IvParameterSpec ivSpec = new IvParameterSpec(iv);
            cipher.init(Cipher.DECRYPT_MODE, keySpec, ivSpec);

            byte[] result = cipher.doFinal(message);
            String retVal = new String(result);
            trace(retVal);

            data.putUtfString("msg", retVal);
        } catch (NoSuchAlgorithmException | NoSuchPaddingException | InvalidKeyException | IllegalBlockSizeException | BadPaddingException | InvalidAlgorithmParameterException e) {
            e.printStackTrace();
        }

        Room room = getParentExtension().getParentRoom();
        getApi().sendExtensionResponse("chat.msg", data, user, room, false);
    }
}