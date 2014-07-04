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

    $('button.accept_invite').click(function(event) {
        var that =$(this);
        var invite_id = that.attr('data');
        var csrf_token = that.attr('csrf_token');
        $.ajax({
            beforeSend: function(xhr, settings) {
                if (!this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrf_token);
                }
            },
            type: "POST",
            url: '/counter/accept_invite/',
            data: { 'invite_id':invite_id },
        })
         .done(function(data) {
            //$('#timer').show();
            $('#invite_accepted').show().fadeOut();
        });

        event.preventDefault();
    });

    var getDateDiffText = function(date_diff) {
        var date_diff_text = "";
        if (date_diff < 1000 * 60) {
            date_diff_text = "Updated Just Now";
        } else if(date_diff < 1000 * 60 * 15) {
            date_diff_text = "Updated a Few Minutes Ago";
        } else if(date_diff < 1000 * 60 * 30) {
            date_diff_text = "Updated a Half-Hour Ago";
        } else if(date_diff < 1000 * 60 * 60 * 2) {
            date_diff_text = "Updated About an Hour Ago";
        } else if(date_diff < 1000 * 60 * 60 * 12) {
            date_diff_text = "Updated a Few Hours Ago";
        } else if(date_diff < 1000 * 60 * 60 * 24 * 2) {
            date_diff_text = "Updated About a Day Ago";
        } else if(date_diff < 1000 * 60 * 60 * 24 * 5) {
            date_diff_text = "Updated a Few Days Ago";
        } else if(date_diff < 1000 * 60 * 60 * 24 * 7 * 2) {
            date_diff_text = "Updated About a Week Ago";
        } else if(date_diff < 1000 * 60 * 60 * 24 * 7 * 3 ) {
            date_diff_text = "Updated a Few Weeks Ago";
        } else if(date_diff < 1000 * 60 * 60 * 24 * 7 * 4 * 2) {
            date_diff_text = "Updated About a Month Ago";
        } else if(date_diff < 1000 * 60 * 60 * 24 * 7 * 4 * 10 ) {
            date_diff_text = "Updated a Few Months Ago";
        } else if(date_diff < 1000 * 60 * 60 * 24 * 365 * 2 ) {
            date_diff_text = "Updated About a Year Ago";
        }
        return date_diff_text;
    }

    $('span.event_timer').each(function(index, element) {
        $el = $(element);
        var event_id = $el.attr('event-id');
        var updated_date = $el.attr('updated-date');

        var updatedDateObject = new Date(Date.parse(updated_date));
        var nowDateObject = new Date();
        $el.text(getDateDiffText(nowDateObject.getTime()-updatedDateObject.getTime()));
    });

    var time_zone = jstz.determine().name();
    $('span.log_time').each(function(index, element) {
        $el = $(element);
        var updated_date = $el.attr('updated-date');
        var converted_date_time_string = moment(updated_date).tz(time_zone).format("MMM D YYYY, h:mma");
        $el.text(converted_date_time_string);
    });
   

});
