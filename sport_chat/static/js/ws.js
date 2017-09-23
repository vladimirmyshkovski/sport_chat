    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    socket = new WebSocket(ws_scheme + "://" + window.location.host + "/chat/" + room); //+ "room_1/" + "team_1/");

    socket.onmessage = function(e) {
      data = JSON.parse(e.data);
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

    }

    socket.onopen = function() {
      socket.send(" connected to chat");
    }

    socket.onclose = function() {
      socket.send(" disconnected from chat");   
    }

    if (socket.readyState == WebSocket.OPEN) socket.onopen();