$(document).ready(function() {
    var d = $(document),
        w = $(window);
        
    var format_all_timestamps = function() {    
        $('.timeago').timeago();
    };
    
    var setup_endless_scroll = function() {
        var find_next_page_link = function() {
                return $('#next-link')
            },
            is_page_end = function() {
                var OFFSET = 2;
                return (OFFSET + w.scrollTop() >= d.height() - w.height());
            },
            extract_url = function(next_link) {
                var a = next_link.find("a[rel='next']");
                return a ? a.attr('href') : false;
            },
            append_next_page = function(data, next_link) {
                next_link.after(data);
                next_link.remove();
                format_all_timestamps();
            };
            
        w.scroll(function() {
            if (!is_page_end()) { return; }
            
            var next_link = find_next_page_link(),
                      url = extract_url(next_link);
            if (!url) { return; }
            
            next_link.show(); 
            
            $.get(url, function(data) {
                append_next_page(data, next_link);
            });
        });
    };
     
    setup_endless_scroll();
    format_all_timestamps();
     
 });