$(document).ready(function() {
    var content = $('#content'),
        submit = $('#submit'),
        count = $('#count');
    
    var update_count = function(diff) {
        count.html(diff);
        count.css('color', (diff < 0) ? 'red' : 'gray');
    };
    
    var validate_content = function() {
        var disable = function(el) { el.attr('disabled', 'disabled'); },
            enable  = function(el) { el.removeAttr('disabled'); };
        
        var content_val = content.val(),
            diff = MAX_LENGTH - content_val.length,
            within_limit = diff >= 0,
            not_blank = $.trim(content_val).length != 0;
        
        update_count( diff );
        
        var content_valid = function() {
            return within_limit && not_blank;
        }
        if (content_valid()) {
            enable(submit);
        } else {
            disable(submit);
        }
    };
    
    var setup_validation = function() {
        content.bind('mouseenter mouseleave keyup', function() {
            validate_content();
        });
        validate_content();
    };

    setup_validation();
});