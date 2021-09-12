package cpi.server.handlers.event;

import com.smartfoxserver.v2.SmartFoxServer;
import com.smartfoxserver.v2.api.ISFSMMOApi;
import com.smartfoxserver.v2.core.ISFSEvent;
import com.smartfoxserver.v2.core.SFSEventParam;
import com.smartfoxserver.v2.entities.*;
import com.smartfoxserver.v2.entities.variables.SFSUserVariable;
import com.smartfoxserver.v2.entities.variables.UserVariable;
import com.smartfoxserver.v2.exceptions.SFSException;
import com.smartfoxserver.v2.extensions.BaseServerEventHandler;
import com.smartfoxserver.v2.mmo.Vec3D;

import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;

public class JoinZone extends BaseServerEventHandler {
    @Override
    public void handleServerEvent(ISFSEvent event) throws SFSException {
        User user = (User) event.getParameter(SFSEventParam.USER);

        DateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd");
        Date date = new Date();
        String dateStr = dateFormat.format(date);

        // TODO: Dynamic room generation.
        String nameOfRoom = "Alpine:en_US:Town::1.13.0;offline;" + dateStr + ";NONE";
        Room roomObj = getParentExtension().getParentZone().getRoomByName(nameOfRoom);

        ISFSMMOApi mmoApi = SmartFoxServer.getInstance().getAPIManager().getMMOApi();

        trace("JOIN_ZONE " + nameOfRoom);

        int sessionId = user.getSession().getId();
        String session = Integer.toString(sessionId);

        ArrayList<UserVariable> varList = new ArrayList<>();
        varList.add(new SFSUserVariable("sess", session));
        varList.add(new SFSUserVariable("loc", 0));

        getApi().setUserVariables(user, varList);
        getApi().joinRoom(user, roomObj);

        // Set our user position.
        mmoApi.setUserPosition(user, new Vec3D(0, 0, 0), roomObj);

        // Debugging
        trace("User (" + sessionId + ") " + user.getName() + ": Set pos to 0/0/0");
        trace("Users in room: " + roomObj.getUserList().size());
    }
}