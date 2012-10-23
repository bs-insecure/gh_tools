function styleForm(){
    // apply styling to form elements
	console.log('test');
    $('input').attr('autocomplete', 'off');
    $('label').addClass('span2');
    $('input, select, textarea').addClass('input-xlarge');
    $('.icon-info-sign').popover();
}

// custom configuration for knockout validation plugin
// see https://github.com/ericmbarnard/Knockout-Validation
ko.validation.configure({
    errorMessageClass: 'help-inline',
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
     if (val === 'ok'){
         self.isDismissVisible(false);
         self.info("Please wait ...")
         self.message("<b>Processing request.</b>");
         self.footer("<b>Thank you for your patience.</b>");
     }
     else {
         self.info('Error!');
         self.message("<b>An error occurred </b>");
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
	self.first_name = ko.observable('test');
	self.last_name = ko.observable();
	self.email = ko.observable();
	
	self.password_old = ko.observable();
	self.password_new = ko.observable();
	self.password_check = ko.observable();
	
	self.errors = ko.validation.group(self);
	
	self.first_name.subscribe(function(val){
		self.last_name(val);
	})
	
	self.countErrors = function(){
		return self.errors.length
	}
	
	self.postData = function(){
		return {
				first_name: self.first_name(),
				last_name: self.last_name(),
				email: self.mail(),
				password_old: self.password_old(),
				password_new: self.password_new
		}
	}
	
}



