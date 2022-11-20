//require Statements
var request = require('request-promise');
const url = require('url');
const path = require('path');
const {spawn} = require('child_process');
const { app, BrowserWindow, Menu, ipcMain, Notification} = require(
    'electron');

var lastAngry = 0
let MainWindow;
let SettingsWindow;
var recording = false;

// Listen for the app to ready:
app.on('ready', function () {
    MainWindow = new BrowserWindow({
        autoHideMenuBar: true,
        frame: false,
        webPreferences: {nodeIntegration: true, contextIsolation: false, enableRemoteModule: true},
        width:1600,
        height: 900});
    MainWindow.loadURL(url.format({
        pathname: path.join(__dirname, 'HTML Templates/Home.html'),
        protocol: 'file:',
        slashes: true,
        
        
    }));

    MainWindow.removeMenu()

    MainWindow.on('closed', function(){
        app.quit(); 
    })

    MainWindow.on('close', function(){
        killServer()
    })

    const mainMenu = Menu.buildFromTemplate(mainMenuTemplate);

    Menu.setApplicationMenu(mainMenu);
    const childPython = spawn('python3', ['backend/server.py']);
    childPython.stdout.on('data', (data) => {
        console.log(`stdout: ${data}`)
    })
    childPython.stderr.on('error', (error) => {
        console.log(`${error}`)
    } )
    childPython.on("close", (code) => {
        console.log(`exited on code: ${code}`)
    })
    startLoop()
});

//Start Loop For Recording
function startLoop(){
    setTimeout(() => {
        if(recording){
            const Data = record();
            console.log("recording")
            isAngry()
        }
        startLoop();
    }, 500)
}

//Send the Angry Notification
function sendAngryNotification(){
    lastAngry = 15
    new Notification({title: "AppThatRecordsYou", body:'Woah! Calm down and try to smile!'}).show()
}

// Create Main Menu Template
const mainMenuTemplate = [
    {
        label: 'File',
        submenu: [
            {
                label: 'Quit',
                accelerator: process.platform == 'darwin' ? 'Command+Q' : 'Ctrl+Q',
                click() {
                    app.quit();
                }
            }
        ]
    }
];

//check how angry user is
async function isAngry() {
	var data = {
	}

	var options = {
		method: 'POST',
        timeout: 180000,
		uri: 'http://127.0.0.1:5000/isangry',
		json: true
	};

	var sendrequest = await request(options)
		.then(function (parsedBody) {
			let result;
			result = parsedBody['isangry'];
            if (result && lastAngry <= 0) {
                console.log("angry")
                sendAngryNotification()
            }
            else{
                lastAngry = lastAngry - 1
            }
            return result;
		})
		.catch(function (err) {
			console.log(err);
            return 0;
		});
}

//record an image
async function record() {
    // console.log('recording');
	var data = {
        "photoSize": 1
	}

	var options = {
		method: 'POST',
        timeout: 180000,
		uri: 'http://127.0.0.1:5000/takeimage',
		body: data,
		json: true
	};

	var sendrequest = await request(options)
		.then(function (parsedBody) {
			let result;
            console.log(parsedBody);
			result = parsedBody['emotions'];
            console.log(result);
            MainWindow.webContents.send("data:update", result[5], result[2], result[7], result[6], result[4], result[3]);
            console.log(result)
            return parsedBody['emotions'];
		})
		.catch(function (err) {
			console.log(err);
            return 0;
		});
}

//get summary data
async function summarize(emotion1, emotion2, emotion3, comparing){
	var data = {
        "emotion1": emotion1,
        "emotion2": emotion2,
        "emotion3": emotion3,
        "comparing": comparing
	}

    var options = {
		method: 'POST',
		uri: 'http://127.0.0.1:5000/summarize',
		body: data,
		json: true
	};

	var sendrequest = await request(options)
		.then(function (parsedBody) {
			let result;
            appEmo = parsedBody['result'];
            var keys = Object.keys(appEmo);
            var values = Object.values(appEmo);
            var topSixKeys = keys.slice(Math.max(-5, -keys.length))
            var topSixValues = values.slice(Math.max(-5, -keys.length))
            MainWindow.webContents.send("emotion:summary", topSixKeys, topSixValues)
            return result;
		})
		.catch(function (err) {
			console.log(err);
            return 0;
		});
}

//kill Server
async function killServer() {
    
    var options = {
		method: 'POST',
		uri: 'http://127.0.0.1:5000/kill',
		json: true
	};

	var sendrequest = await request(options)
		.then(function (parsedBody) {
			let result;
		})
		.catch(function (err) {
			console.log(err);
		});
}

//fucntion to end session
async function endSession(){

    var options = {
		method: 'POST',

		uri: 'http://127.0.0.1:5000/endsession',
		json: true
	};

	var sendrequest = await request(options)
		.then(function (parsedBody) {
			let result;
		})
		.catch(function (err) {
			console.log(err);
		});
}

//function to create settings window
function createSettingsWindow(){
    
    SettingsWindow = new BrowserWindow({
        width: 1200, 
        height: 820, 
        title: 'Settings',
        resizable: false, 
        fullscreen: false,
        webPreferences: {nodeIntegration: true, contextIsolation:false} 
    });

    SettingsWindow.loadURL(url.format({
        pathname: path.join(__dirname, 'HTML Templates/Settings.html'),
        protocol: 'file:',
        slashes: true
    }));

    SettingsWindow.on('close', function(){
        SettingsWindow=null
    });
}

function createHelpWindow(){
    
    SettingsWindow = new BrowserWindow({
        width: 1200, 
        height: 820, 
        title: 'Find a Therapist near you!',
        resizable: false, 
        fullscreen: false,
        webPreferences: {nodeIntegration: true, contextIsolation:false} 
    });

    SettingsWindow.loadURL("https://www.google.com/maps/search/Therapists+Near+Me/@37.6,-95.7528906");

    SettingsWindow.on('close', function(){
        SettingsWindow=null
    });
}


//listener to open settings
ipcMain.on("open:settings", function(e){
    if(SettingsWindow==null){
        createSettingsWindow();
    }
    else{
        SettingsWindow.show();
    }
})
ipcMain.on("open:TPHELP", function(e){
    if(SettingsWindow==null){
        createHelpWindow();
    }
    else{
        SettingsWindow.show();
    }
})
//listener to change recording status
ipcMain.on("recorder:change", function(e){
    recording=!recording;
    if (!recording){
        endSession();
    }
});

ipcMain.on('app:quit', () => { app.quit() })

//listener to start summary maker
ipcMain.on("summary:emotions", function(e, emotion1, emotion2, emotion3, comparing){
    var appEmo = summarize(emotion1, emotion2, emotion3, comparing)
})