package cpi.server;

import com.smartfoxserver.v2.extensions.SFSExtension;

import cpi.server.handlers.request.GetTime;
import cpi.server.handlers.request.GetEncryption;
import cpi.server.handlers.request.ZoneLogout;
import cpi.server.handlers.request.LocoMotionAction;

// Chat
import cpi.server.handlers.request.chat.ActivityCancel;
import cpi.server.handlers.request.chat.Message;
import cpi.server.handlers.request.chat.Activity;

public class RequestHandler extends SFSExtension {
    @Override
    public void init()
    {
        trace("Registering request handlers...");

        addRequestHandler("time.get", GetTime.class);
        addRequestHandler("encryption.get", GetEncryption.class);
        addRequestHandler("zone.logout", ZoneLogout.class);
        addRequestHandler("l.a", LocoMotionAction.class);
        addRequestHandler("chat.msg", Message.class);
        addRequestHandler("chat.activity", Activity.class);
        addRequestHandler("chat.activity_cancel", ActivityCancel.class);

        trace("Request handlers active!");
    }
}