package cpi.server.handlers.request;

// Server
import com.smartfoxserver.v2.entities.Room;
import com.smartfoxserver.v2.entities.data.ISFSObject;
import com.smartfoxserver.v2.entities.data.SFSObject;
import com.smartfoxserver.v2.extensions.BaseClientRequestHandler;
import com.smartfoxserver.v2.entities.User;

// Cryptography
import javax.crypto.BadPaddingException;
import javax.crypto.Cipher;
import javax.crypto.IllegalBlockSizeException;
import javax.crypto.NoSuchPaddingException;
import java.math.BigInteger;
import java.security.*;
import java.security.spec.InvalidKeySpecException;
import java.security.spec.RSAPublicKeySpec;
import java.util.Base64;

public class GetEncryption extends BaseClientRequestHandler {
    public static byte[] encryptRSA(String str, PublicKey pubKey) throws NoSuchAlgorithmException, NoSuchPaddingException, InvalidKeyException, IllegalBlockSizeException, BadPaddingException, NoSuchProviderException {
        Cipher cipher = Cipher.getInstance("RSA/ECB/PKCS1Padding");
        cipher.init(Cipher.ENCRYPT_MODE, pubKey);
        return cipher.doFinal(str.getBytes());
    }

    @Override
    public void handleClientRequest(User user, ISFSObject params) {
        String modulus = params.getUtfString("pkm");
        String exponent = params.getUtfString("pke");
        trace("GET_ROOM_ENCRYPTION_KEY " + modulus + " " + exponent);

        ISFSObject data = new SFSObject();

        try {
            byte[] modulusByte = Base64.getDecoder().decode(modulus);
            byte[] exponentByte = Base64.getDecoder().decode(exponent);

            BigInteger modulusAsBigInt = new BigInteger(1, modulusByte);
            BigInteger exponentAsBigInt = new BigInteger(1, exponentByte);

            RSAPublicKeySpec spec = new RSAPublicKeySpec(modulusAsBigInt, exponentAsBigInt);
            KeyFactory factory = KeyFactory.getInstance("RSA");
            PublicKey publicKey = factory.generatePublic(spec);

            byte[] encrypted = encryptRSA("dZJrQkW32sXkeVF9G3Zc0jeO7UzCUEhs", publicKey);
            String encKey = Base64.getEncoder().encodeToString(encrypted);
            trace(publicKey);
            data.putUtfString("ek", encKey);
        } catch (NoSuchAlgorithmException | InvalidKeySpecException | NoSuchPaddingException | InvalidKeyException | IllegalBlockSizeException | BadPaddingException | NoSuchProviderException e) {
            e.printStackTrace();
        }

        // Send our response to the client.
        Room room = getParentExtension().getParentRoom();
        getApi().sendExtensionResponse("encryption.get", data, user, room, false);
    }
}