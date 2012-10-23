function styleForm(){
    // apply styling to form elements
    $('input').attr('autocomplete', 'off');
    $('label').addClass('span2');
    $('input, select, textarea').addClass('input-xlarge');
    $('.icon-info-sign').popover();
}

// custom configuration for knockout validation plugin
// see https://github.com/ericmbarnard/Knockout-Validation
ko.validation.configure({
    errorMessageClass: 'help-inline error',
    errorElementClass: 'error',
    decorateElement: true
})

// validation rule, checks if a value is within a given array
ko.validation.rules['isValidValue'] = {
    validator: function (val, array) {
        return $.inArray(val, array) === -1 ? false : true;
    },
    message: 'Please choose a valid value.'
};

// validation rule, returns true if the value is an integer
ko.validation.rules['isInt'] = {
    validator: function (value, validate) {
        return validate && /^[0-9]+$/.test(value);
    },
    message: 'An integer value is required.'
}

ko.validation.rules['mustEqual'] = {
	    validator: function (val, otherVal) {
	        return val === otherVal;
	    },
	    message: 'The field must equal {0}'
	};

ko.validation.rules['isLater'] = {
	validator: function (value, validate) {
		return (new Date(value) >= validate);
	},
	message: 'The date must be in the future.'
}

// validation rule, checks if a value is already within an array
ko.validation.rules['uniqueItem'] = {
    validator: function(val, array) {
        var count = 0;
        $.each(array, function(i, v) {if (v === val) count++;});
        return count > 1 ? false : true;
    },
    message: 'Please provide unique hostnames.'
};

ko.validation.rules['isFutureDate'] = {
    validator: function (val, validate) {
        var pickedDateParts = val.split("/");
        var pickedDate = new Date(pickedDateParts[2], (pickedDateParts[1] - 1), pickedDateParts[0]);
        return validate && (pickedDate > new Date())
    },
    message: 'Please select a date in the future.'
}

ko.validation.rules['isIPRange'] = {
    validator: function (value, validate) {
        return validate && /^(([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])[.]){3}([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])[\/]([0-2]?[0-9]|3[0-2])$/.test(value);
    },
    message: 'Please provide a valid IP-Range.'
}

ko.validation.registerExtenders();



function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

//ko model
//feed the error property with a value and all other properties
//change their values accordingly
function Modal(){
 var self = this;
 self.info = ko.observable();
 self.message = ko.observable();
 self.footer = ko.observable();
 self.error = ko.observable();
 self.isDismissVisible = ko.observable();
 self.imageModal = ko.observable();



 self.error.subscribe(function(val){
     $('.modal').css('width', '400px');
     self.isDismissVisible(true);
     console.log('..', val);
     if (val === 'ok'){
         self.isDismissVisible(false);
         self.info("Please wait ...")
         self.message("<b>Processing request.</b>");
         self.footer("<b>Thank you for your patience.</b>");
     }
     else {
         self.info('Error!');
         self.message("<b>An error occurred: "+val+" </b>");
     }
 });

 self.imageModal.subscribe(function(imageurl){
     $('.modal').css('width', '850px');
     self.isDismissVisible(true);
     self.info('Image');
     self.message(imageurl);
 });
}

function AccountViewModel()
{
	var self = this;
	self.modal = ko.observable(new Modal());
	self.username = ko.observable(user_username);
	self.first_name = ko.observable(user_first_name);
	self.last_name = ko.observable(user_last_name);
	self.email = ko.observable(user_email).extend({ email: true });
	
	self.password_old = ko.observable().extend({required: true});
	self.password_new = ko.observable();
	self.password_check = ko.observable();
	
	self.response_status = ko.observable();
	self.response_message = ko.observable();
	
	self.errors = ko.validation.group(self);
	
	self.password_new.subscribe(function(val){
	   self.password_check.rules.remove(function(x) { return x.rule === "mustEqual" });
       self.password_check.extend({ mustEqual: { message: 'The passwords must match.',
	                                         params: self.password_new()}});
	})
	
	self.response_status.subscribe(function(val){
		if (val == 'success'){
			$("#AccountForm :input").attr("disabled", true);
		}
	})
	
	self.countErrors = function(){
		return self.errors().length
	}
	
	self.post_data = function(){
		return {
				first_name: self.first_name(),
				last_name: self.last_name(),
				email: self.email(),
				password_old: self.password_old(),
				password_new: self.password_new(),
				username: self.username()
		}
	}
	
	self.showAllErrors = function(){
		self.errors.showAllMessages();
	}
	
	self.submit = function() {
        if (self.countErrors() > 0){
            self.showAllErrors();
        }
        else {
        	var csrftoken = getCookie('csrftoken');
        	
        	$.ajaxSetup({
        	    crossDomain: false, // obviates need for sameOrigin test
        	    beforeSend: function(xhr, settings) {
        	        if (!csrfSafeMethod(settings.type)) {
        	            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        	        }
        	    }
        	});
            $.post( '/account/', $.param(ko.toJS(self.post_data()), true), function(data){
                response = $.parseJSON(data);
                self.response_status(response.status);
                self.response_message(response.message);
                }
            );
        }
    }
	
}



