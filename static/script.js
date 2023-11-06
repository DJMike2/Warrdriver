let Mode;
let BSSID;
let socket;
let OVR;
let ID;
let buttonNumber;
function SOCKET_NETWORKS(URL){
    const messageContainer = document.getElementById('message-container');

    // Create a WebSocket connection
    socket = new WebSocket(URL); // URL

    // WebSocket event listeners
    socket.addEventListener('open', function (event) {
        console.log('WebSocket connection opened:', event);
    });

    socket.addEventListener('message', function (event) {
        // Handle incoming WebSocket messages
        const incoming = event.data
        const newData = JSON.parse(incoming); //JSON FORMAT DEALT WITH ERROR DUE TO IT NOT BEING FORMATTED

        //console.log('Received data:', newData);
        network_info = ['ESSID', 'BSSID', 'Enc', 'Cipher', 'Auth', '2.4GHz or 5GHz', 'Channel', 'PWR', 'Beacons'];

        OVR = [];

        //Generates Array from API
        for (let i = 0; i < newData.length; i++) {
            const DATA = [];
            for (let x = 0; x < network_info.length; x++) {
                DATA.push(newData[i][i][network_info[x]]);

            }
            OVR.push(DATA);
        }
        console.log(OVR);
        console.log('finished')
        // Clear existing table rows
        const table = document.querySelector("table");
        while (table.rows.length > 1) {
            table.deleteRow(1); // Delete all rows except the header row
        }

        // Function to create table rows
        function createTableRows() {
            const table = document.querySelector("table");

            let x = 0;
            for (const rowData of OVR) {
                const row = table.insertRow();
                const BT = document.createElement('button');
                // Step 3: Set the button's class and inline styles
                BT.className = "fa fa-gear"; // Add the classes
                BT.style.fontSize = "18px"; // Set the font size
                BT.style.color = "red"; // Set the color
                BT.setAttribute('data-button-number', x);
                x+=1

                BT.onclick = function() {
                    buttonNumber = this.getAttribute('data-button-number');
                    console.log(buttonNumber);
                    Focus(buttonNumber);
                };

                document.body.appendChild(BT);
                for (const cellData of rowData) {
                    const cell = row.insertCell();
                    cell.textContent = cellData;
                    row.appendChild(BT);
                    //console.log(cellData);
                }
            }
        }
        createTableRows(); //CALL THE FUNCTION
    });

    socket.addEventListener('close', function (event) {
        console.log('WebSocket connection closed:', event);
    });

    socket.addEventListener('error', function (event) {
        console.error('WebSocket error:', event);
    });
};



function SOCKET_DEVICES(URL){
    setTimeout(3000)
    const messageContainer = document.getElementById('message-container');

    // Create a WebSocket connection
    socket = new WebSocket(URL); // URL

    // WebSocket event listeners
    socket.addEventListener('open', function (event) {
        console.log('WebSocket connection opened:', event);
    });

    socket.addEventListener('message', function (event) {
        // Handle incoming WebSocket messages
        const incoming = event.data
        const newData = JSON.parse(incoming); //JSON FORMAT DEALT WITH ERROR DUE TO IT NOT BEING FORMATTED
        console.log(newData);
        //console.log('Received data:', newData);
        network_info = ['client-mac', 'client-manuf', 'channel', 'encoding', 'PWR', 'carrier'];
        //wireless-client | client-mac | client-manuf | channel | encoding | carrier | snr-info][last_signal_dbm] 7/9

        const OVR = []; //Array of data

        //Generates an array from API
        for (let i = 0; i < newData.length; i++) {
            const DATA = [];
            for (let x = 0; x < network_info.length; x++) {
                DATA.push(newData[i][i][network_info[x]]);

            }
            OVR.push(DATA);
        }
        console.log(OVR);
        console.log('finished')
        // Clear existing table rows
        const table = document.querySelector("table");
        while (table.rows.length > 1) {
            table.deleteRow(1); // Delete all rows except the header row
        }
        // Function to create table rows
        function createTableRows() {
            const table = document.querySelector("table");

            for (const rowData of OVR) {
                const row = table.insertRow();
                const BT = document.createElement('button');
                // Step 3: Set the button's class and inline styles
                BT.setAttribute('data-row-id', rowData.id);
                BT.className = "fa fa-gear"; // Add the classes
                BT.style.fontSize = "18px"; // Set the font size
                BT.style.color = "red"; // Set the color


                document.body.appendChild(BT);
                for (const cellData of rowData) {
                    const cell = row.insertCell();
                    cell.textContent = cellData;
                    row.appendChild(BT);
                    //console.log(cellData);
                }
            }
        }
        createTableRows(); //CALL THE FUNCTION
    });

    socket.addEventListener('close', function (event) {
        console.log('WebSocket connection closed:', event);
    });

    socket.addEventListener('error', function (event) {
        console.error('WebSocket error:', event);
    });
};

function closeWebSocket() {
    if (socket && socket.readyState === WebSocket.OPEN) {
        socket.close();
    }
    console.log("CLOSED SOCKET!");
};


function SCAN_START() {
    console.log(Mode);
    if (Mode === 'Networks'){
        fetch('/', {
            method: 'POST',
            body: new URLSearchParams({ 'action': 'Start'}),  // Form data with 'action' parameter
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        })
        .then(response => response.text())
        .then(data => {
            console.log(data);  // Log the response from the server
        })
        .catch(error => {
            console.error('An error occurred:', error);
        });
    }
    else if (Mode === 'Devices'){
        BSSID = OVR[ID][1];
        console.log(BSSID)
        fetch('/', {
            method: 'POST',
            body: new URLSearchParams({ 'action': 'Start', 'Mode': Mode, 'BSSID':BSSID}),  // Form data with 'action' parameter
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        })
        .then(response => response.text())
        .then(data => {
            console.log(data);  // Log the response from the server
        })
        .catch(error => {
            console.error('An error occurred:', error);
        });
    }
}

function SCAN_STOP() {
    fetch('/', {
        method: 'POST',
        body: new URLSearchParams({ 'action': 'stop' }),  // Form data with 'action' parameter
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    })
    .then(response => response.text())
    .then(data => {
        console.log(data);  // Log the response from the server
    })
    .catch(error => {
        console.error('An error occurred:', error);
    });
}





async function START_LOOP_NETWORKS() {
    Mode = 'Networks';
    try {
        const payPromise = SOCKET_NETWORKS('ws://localhost:8000/network-feed');
        const clsPromise = SCAN_START();

        await Promise.all([payPromise, clsPromise]);

        console.log("Both functions have finished concurrently");
    } catch (error) {
        console.error("An error occurred:", error);
    }
}
async function STOP_LOOP_NETWORKS() {
    try {
        const payPromise = closeWebSocket();
        const clsPromise = SCAN_STOP();

        await Promise.all([payPromise, clsPromise]);

        console.log("Both functions have finished concurrently");
    } catch (error) {
        console.error("An error occurred:", error);
    }
}





function Clear_Table() {
    $('td').remove();
    $('.fa.fa-gear').remove();

    var textValues = ["client-mac", "client-manuf", "channel", "encoding", "carrier", "PWR"];
    var thElements = $("th");

    thElements.each(function(index) {
      if (index < textValues.length) {
        $(this).text(textValues[index]);
      } else {
        // If there are more th elements than text values, remove the extra elements
        $(this).remove();
      }
    });

}


async function Focus(BTNUM) {
    console.log('FOcus');
    Mode = 'Devices';
    console.log(BTNUM); //Null???
    ID = BTNUM
    try {
        const clsPromise2 = SCAN_START();
        const payPromise = SOCKET_DEVICES('ws://localhost:8000/device-feed'); // start device socket
        const clsPromise = Clear_Table(); // clear table and stop any current scans for future

        await Promise.all([payPromise, clsPromise, clsPromise2]);

        console.log("Both functions have finished concurrently");
    } catch (error) {
        console.error("An error occurred:", error);
    }
}