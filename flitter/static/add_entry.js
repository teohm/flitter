$(document).ready(function() {
    var entries = $('#entries')
        form = $('#entry-form'),
        content = $('#content'),
        submit = $('#add'),
        count = $('#count');
    
    var update_char_count = function(diff) {
        count.html(diff);
        count.css('color', (diff < 0) ? 'red' : 'gray');
    };
    
    var validate_content = function() {
        var content_val = content.val(),
            diff = FLTR.MAX_LENGTH - content_val.length,
            within_limit = diff >= 0,
            not_blank = $.trim(content_val).length != 0;
        
        var disable = function(el) { el.attr('disabled', 'disabled'); },
            enable  = function(el) { el.removeAttr('disabled'); },
            content_valid = function() {
                return within_limit && not_blank;
            };
        
        update_char_count( diff );
        
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
    
    var setup_ajax_submit = function() {
        var update_timestamps = function() {
                $(".timeago").timeago();
            },
            reset_form = function() {
                content.val('');
                validate_content();
            },
            show_entry = function(data) {
                entries.prepend(data);
                update_timestamps();
            };
            
        form.submit(function(ev) {
            ev.preventDefault();
            $.ajax({
                url: form.attr('action'),
                type: form.attr('method'),
                data: form.serialize(),
                success: function(data) { show_entry(data); }
            });
            reset_form();
        });
    };

    setup_validation();
    setup_ajax_submit();
});