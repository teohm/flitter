$(document).ready(function() {
    var username = $('#username'),
        password = $('#password'),
        submit = $('#submit'),
        username_hint = $('#username-hint'),
        password_hint = $('#password-hint');
        
    var validate_signup = function() {            
        var username_valid = function() {
                return /^[0-9a-zA-Z]{3,12}$/.test(username.val());
            },
            password_valid = function() {
               return /^.{6,16}$/.test(password.val());
            };
        var disable = function(el) { el.attr('disabled', 'disabled'); },
            enable  = function(el) { el.removeAttr('disabled'); };

        if (username_valid() && password_valid()) {
            enable(submit);
        } else {
            disable(submit);
        }
    };
    
    var setup_validation = function() {    
        $.each([username, password], function(idx, input) {
            input.bind('change keypress', function() {
                validate_signup();
            });
        });
        validate_signup();
    };
    
    var setup_hints = function() {
        username.
            focus(function() { username_hint.show(); }).
            blur(function()  { username_hint.hide(); });
        username_hint.hide();
        
        password.
            focus(function() { password_hint.show(); }).
            blur(function()  { password_hint.hide(); });
        password_hint.hide();
    };
    
    setup_validation();
    setup_hints();
});