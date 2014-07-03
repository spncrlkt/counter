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

    $('form#add_event').submit(function(event) {
        var that =$(this);
        var csrf_token = that.attr('csrf_token');
        $.ajax({
            beforeSend: function(xhr, settings) {
                if (!this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrf_token);
                }
            },
            type: "POST",
            url: '/counter/add/',
            data: that.serialize(),
        })
         .done(function(data) {
            //$('#timer').show();
            $('#added').show().fadeOut();
        });

        event.preventDefault();
    });

    $('form#add_event_permission').submit(function(event) {
        var that =$(this);
        var event_id = that.attr('event_id');
        var csrf_token = that.attr('csrf_token');
        $.ajax({
            beforeSend: function(xhr, settings) {
                if (!this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrf_token);
                }
            },
            type: "POST",
            url: '/counter/'+event_id+'/add_permission/',
            data: that.serialize(),
        })
         .done(function(data) {
            //$('#timer').show();
            $('#event_permission_sent').show().fadeOut();
        });

        event.preventDefault();
    });
})
