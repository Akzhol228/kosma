const roomId = JSON.parse(
    document.getElementById('room-split-1-id').textContent
)
const demandDistributionIdActive = JSON.parse(
    document.getElementById('room-split-2-id').textContent
)
const requestUser = JSON.parse(
    document.getElementById('request-user').textContent
)
const url = 'ws://' + window.location.host + '/ws/chat/' + roomId + '/room/'
const chatSocket = new WebSocket(url)

chatSocket.onmessage = function(event) {
    var output = ''
    const data = JSON.parse(event.data)
    var demandDistributionId = data.demand_distribution_id
    const dateOptions = {hour: 'numeric', minute: 'numeric', hour24: true};
    const datetime = new Date(data.datetime).toLocaleString('en', dateOptions);
    const isMe = data.user === requestUser;
    const source = isMe ? 'd-flex' : 'media-chat-reverse';
    const name = isMe ? 'Me' : data.user;
    var is_active = demandDistributionIdActive == demandDistributionId
    if(is_active){
        output += '<div class="media media-chat ' + source + '">'
        output += '<div class="media-body">'
        output += '<p>' + data.message + '</p>'
        $('#chat-content').append(output).animate({ scrollTop: 200000 }, "slow")
    }
    else{
        var notification_chat_id = '#notification-chat-' + demandDistributionId
        var notification_chat = parseInt($(notification_chat_id).html())
        if(notification_chat){
            notification_chat += 1
        }
        else{
            notification_chat = 1
        }
        $(notification_chat_id).html(notification_chat)

    }
}

chatSocket.onclose = function(event) {
    console.error('Chat socket closed unexpectedly')
}

$(document).on('keypress',function(e) {
    if(e.which == 13) {
        e.preventDefault()
        $('#chat-message-submit').click()
    }
})

$(document).on('click','#chat-message-submit',function(){
    const text = $('#chat-message-input').val()
    $.ajax({
        url: "/chat/message/create",
        type: 'POST',
        data: {
            text: text,
            object_id: demandDistributionIdActive
        },
        success: function(data) {
            $('#chat-message-input').val('').focus()
            chatSocket.send(JSON.stringify({'message': text, 'demand_distribution_id': demandDistributionIdActive}))
        }
    })
})