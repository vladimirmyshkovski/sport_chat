    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    chat_socket = new WebSocket(ws_scheme + "://" + window.location.host + "/chat/" + room); //+ "room_1/" + "team_1/");

    chat_socket.onmessage = function(e) {
      data = JSON.parse(e.data);
      console.log(data)
      if(data.hasOwnProperty('notification_message')){
        alert(data.notification_message);
      } else {
      if (data.room == room) {
      var message = '<div class="col-lg-8 message">' + 
                    '<span style="color: blue">' + data.team + '</span> ' + 
                    '<span style="color: red">' + data.username + '</span> ' +
                    data.message +
                    '</div>'; 
      } else {
      var message = '<div class="col-lg-4 col-lg-offset-4 message" style="text-align: right">' + 
                    '<span style="color: blue">' + data.team + '</span> ' + 
                    '<span style="color: red">' + data.username + '</span> ' +
                    data.message +
                    '</div>'; 
      }
      $('.chat').append(message);
    };
    }


    chat_socket.onopen = function() {
      chat_socket.send(" connected to chat");
    }

    chat_socket.onclose = function() {
      chat_socket.send(" disconnected from chat");   
    }

    if (chat_socket.readyState == WebSocket.OPEN) chat_socket.onopen();


    /*
    notification_socket = new WebSocket(ws_scheme + "://" + window.location.host + "/notification/" + notificationRoom); //+ "room_1/" + "team_1/");


    notification_socket.onopen = function() {
      notification_socket.send(" connected to chat");
    }

    notification_socket.onclose = function() {
      //notification_socket.send(" disconnected from chat");   
    }

    notification_socket.onmessage = function(e) {
      notification_data = JSON.parse(e.data);
      console.log(notification_data);
    }

    if (notification_socket.readyState == WebSocket.OPEN) notification_socket.onopen();    
    */