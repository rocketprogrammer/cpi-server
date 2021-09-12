package cpi.server.handlers.request.chat;

import com.smartfoxserver.v2.entities.Room;
import com.smartfoxserver.v2.entities.data.ISFSObject;
import com.smartfoxserver.v2.entities.data.SFSObject;
import com.smartfoxserver.v2.extensions.BaseClientRequestHandler;
import com.smartfoxserver.v2.entities.User;

public class ActivityCancel extends BaseClientRequestHandler {
    @Override
    public void handleClientRequest(User user, ISFSObject params) {
        trace("CHAT_ACTIVITY_CANCEL + ", params.getDump());

        ISFSObject data = new SFSObject();

        Room room = getParentExtension().getParentRoom();
        getApi().sendExtensionResponse("chat.activity_cancel", data, user, room, false);
    }
}