$(document).ready(function () {
    $('button.reset').click(function() {
        var that =$(this);
        var event_id = that.attr('data');
        alert(event_id);
    });
})
