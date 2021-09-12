package cpi.server;

import cpi.server.handlers.event.Login;
import cpi.server.handlers.event.JoinZone;

import com.smartfoxserver.v2.core.SFSEventType;
import com.smartfoxserver.v2.extensions.SFSExtension;

public class EventHandler extends SFSExtension {
	@Override
	public void init()
	{
		trace("Registering event handlers...");

		addEventHandler(SFSEventType.USER_LOGIN, Login.class);
		addEventHandler(SFSEventType.USER_JOIN_ZONE, JoinZone.class);

		trace("Event handlers active!");
	}
}
