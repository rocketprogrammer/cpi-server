package cpi.server.handlers.request;

import com.smartfoxserver.v2.entities.Room;
import com.smartfoxserver.v2.entities.data.ISFSObject;
import com.smartfoxserver.v2.entities.data.SFSObject;
import com.smartfoxserver.v2.extensions.BaseClientRequestHandler;
import com.smartfoxserver.v2.entities.User;

public class GetTime extends BaseClientRequestHandler {
    @Override
    public void handleClientRequest(User user, ISFSObject params) {
        trace("GET_SERVER_TIME + ", params.getDump());

        long time = params.getLong("ct");

        ISFSObject data = new SFSObject();
        data.putLong("ct", time);
        data.putLong("st", System.currentTimeMillis());

        Room room = getParentExtension().getParentRoom();
        getApi().sendExtensionResponse("time.get", data, user, room, false);
    }
}