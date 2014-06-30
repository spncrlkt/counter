$(document).ready(function () {
    $('button.reset').click(function() {
        var that =$(this);
        var event_id = that.attr('data');
        $.getJSON('/counter/'+event_id+'/reset', function(data) {
            //$('#timer').show();
            $('#updated').show().fadeOut();
        });


    });
})
