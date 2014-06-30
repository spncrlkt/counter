$(document).ready(function () {
    $('button.reset').click(function() {
        var that =$(this);
        var event_id = that.attr('data');
        var csrf_token = that.attr('csrf_token');
        var reset_url = '/counter/'+event_id+'/reset/';
        $.ajax({
            beforeSend: function(xhr, settings) {
                if (!this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrf_token);
                }
            },
            type: "POST",
            url: reset_url,
            data: {'event_id':event_id},
        })
         .done(function(data) {
            //$('#timer').show();
            $('#updated').show().fadeOut();
        });


    });
})
