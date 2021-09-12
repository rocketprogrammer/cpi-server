package cpi.server.handlers.request;

import com.smartfoxserver.v2.entities.Room;
import com.smartfoxserver.v2.entities.data.ISFSObject;
import com.smartfoxserver.v2.entities.data.SFSObject;
import com.smartfoxserver.v2.extensions.BaseClientRequestHandler;
import com.smartfoxserver.v2.entities.User;

public class ZoneLogout extends BaseClientRequestHandler {
    @Override
    public void handleClientRequest(User user, ISFSObject params) {
        trace("ZONE_LOGOUT + ", params.getDump());

        ISFSObject data = new SFSObject();
        data.putUtfString("zone_id", "Town");

        Room room = getParentExtension().getParentRoom();
        getApi().sendExtensionResponse("zone.force_leave", data, user, room, false);
    }
}