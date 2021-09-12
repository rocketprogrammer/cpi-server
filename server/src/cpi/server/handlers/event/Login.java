package cpi.server.handlers.event;

import com.smartfoxserver.bitswarm.sessions.ISession;
import com.smartfoxserver.v2.core.ISFSEvent;
import com.smartfoxserver.v2.core.SFSEventParam;
import com.smartfoxserver.v2.entities.data.ISFSObject;
import com.smartfoxserver.v2.entities.data.SFSObject;
import com.smartfoxserver.v2.extensions.BaseServerEventHandler;

public class Login extends BaseServerEventHandler {
    @Override
    public void handleServerEvent(ISFSEvent event) {
        String userName = (String) event.getParameter(SFSEventParam.LOGIN_NAME);
        String password = (String) event.getParameter(SFSEventParam.LOGIN_PASSWORD);
        ISession session = (ISession) event.getParameter(SFSEventParam.SESSION);

        SFSObject loginInData = (SFSObject) event.getParameter(SFSEventParam.LOGIN_IN_DATA);
        SFSObject data = (SFSObject) SFSObject.newFromJsonData((String) loginInData.getClass("joinRoomData"));

        String zoneName = getParentExtension().getParentZone().getName();

        trace("Logging in, " + userName + "!");
        trace(loginInData.toJson());

        // TODO: Check credentials.
        ISFSObject params = new SFSObject();
        //getApi().login(session, userName, password, zoneName, params);
    }

}
