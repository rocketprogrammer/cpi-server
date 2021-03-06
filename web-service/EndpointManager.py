from aiohttp import web
import logging, asyncio, requests, json

# Setup logging for web requests.
logging.basicConfig(level = logging.INFO)

async def handleRequestApiKey(request):
    data = {
        'success': 1
    }

    headers = {
        'api-key': 'vsKeOpMOZYOH6WPsOZZ7zpulDoxF8Ob5'
    }

    return web.json_response(data, headers = headers)

async def handleGuestLogin(request):
    args = await request.json()

    username = args['loginValue']
    password = args['password']

    response = {}
    return web.json_response(response)

async def handleSiteConfiguration(request):
    data = open('resources/site/configuration.json').read()
    return web.json_response(data)

async def handleRegistrationText(request):
    data = {}
    data['Status'] = 'OK'

    data['RegistrationText'] = [{
        'TextCode': 'gtou_ppv2_proxy_create',
        'Text': ''
    }]

    headers = {
        'api-key': 'vsKeOpMOZYOH6WPsOZZ7zpulDoxF8Ob5'
    }

    return web.json_response(data, headers = headers)

async def handleValidate(request):
    data = {
        'success': 1
    }

    return web.json_response(data)

async def handlePlayer(request):
    data = {
        'minigameProgress': [],
        'quests': [],
        'membershipExpireDate': 0,
        'subscriptionVendor': '',
        'subscriptionProductId': '',
        'subscriptionPaymentPending': False,
        'migrationData': [],
        'tutorialData': [],
        'breadcrumbs': [],
        'claimedRewardIds': [],
        'iglooLayouts': [],
        'trialAvailable': True,
        'recurring': False,
        'dailySpinData': []
    }

    return web.json_response(data)

async def handleRooms(request):
    data = {
        'RoomsFound': [
            'test'
        ]
    }

    return web.json_response(data)

async def initializeService():
    app = web.Application()

    basePath = '/jgc/v5/client/DI-CLUBPENGUINISLANDWIN.GC.SERVER-PROD'

    app.router.add_post('{0}/api-key'.format(basePath), handleRequestApiKey)
    app.router.add_post('{0}/guest/login'.format(basePath), handleGuestLogin)
    app.router.add_get('{0}/configuration/site'.format(basePath), handleSiteConfiguration)
    app.router.add_post('/registration/text', handleRegistrationText)
    app.router.add_post('{0}/validate'.format(basePath), handleValidate)
    app.router.add_get('/game/v1/rooms', handleRooms)
    app.router.add_get('/player/v1/', handlePlayer)

    return app

loop = asyncio.get_event_loop()
app = loop.run_until_complete(initializeService())
web.run_app(app, host = '0.0.0.0', port = 80)