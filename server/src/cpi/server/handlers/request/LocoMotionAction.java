package cpi.server.handlers.request;

// Server
import com.smartfoxserver.v2.SmartFoxServer;
import com.smartfoxserver.v2.api.ISFSMMOApi;
import com.smartfoxserver.v2.entities.Room;
import com.smartfoxserver.v2.entities.data.ISFSObject;
import com.smartfoxserver.v2.entities.data.SFSObject;
import com.smartfoxserver.v2.entities.variables.SFSUserVariable;
import com.smartfoxserver.v2.entities.variables.UserVariable;
import com.smartfoxserver.v2.extensions.BaseClientRequestHandler;
import com.smartfoxserver.v2.entities.User;
import com.smartfoxserver.v2.mmo.Vec3D;

import java.util.ArrayList;
import java.util.Collection;

public class LocoMotionAction extends BaseClientRequestHandler {
    @Override
    public void handleClientRequest(User user, ISFSObject params) {
        trace("LOCOMOTION_ACTION + ", params.getDump());

        int sessionId = user.getSession().getId();
        trace("SESSION_ID", sessionId);

        // We have to convert this to a string.
        // Thanks, Disney!
        String session = Integer.toString(sessionId);

        // Grab the pos of our player from the params.
        Collection<Float> pos = params.getFloatArray("p");

        Object[] objectArray = pos.toArray();
        Float[] floatArray = new Float[objectArray.length];

        for (int i = 0; i < objectArray.length; i++) {
            floatArray[i] = (Float) objectArray[i];
        }

        // Retrieve some data from the client params.
        long timestamp = params.getLong("t");
        byte action = params.getByte("a");

        // Prepare a ArrayList with our user variables.
        ArrayList<UserVariable> varList = new ArrayList<>();
        varList.add(new SFSUserVariable("sess", session));
        varList.add(new SFSUserVariable("loc", action));

        // Update our user variables.
        getApi().setUserVariables(user, varList);

        // Prepare our data response.
        ISFSObject data = new SFSObject();
        data.putByte("a", action);
        data.putFloatArray("p", pos);
        data.putLong("t", timestamp);
        data.putInt("senderId", sessionId);

        // Sometimes, direction is not included in the parameters.
        if (params.containsKey("d")) {
            Collection<Float> direction = params.getFloatArray("d");
            data.putFloatArray("d", direction);
        }

        // Get our MMO API.
        ISFSMMOApi mmoAPi = SmartFoxServer.getInstance().getAPIManager().getMMOApi();

        // Convert our integer position values to float.
        int x = Math.round(floatArray[0]);
        int y = Math.round(floatArray[1]);
        int z = Math.round(floatArray[2]);

        Vec3D posVec = new Vec3D(x, y, z);
        Room room = getParentExtension().getParentRoom();

        // Set our user position.
        mmoAPi.setUserPosition(user, posVec, room);

        // Send our response to the client.
        getApi().sendExtensionResponse("l.a", data, user, room, false);
    }
}