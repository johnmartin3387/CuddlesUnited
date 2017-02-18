var FormValidation = function () {

    // basic validation
    var handleValidation1 = function() {
        // for more info visit the official plugin documentation: 
            // http://docs.jquery.com/Plugins/Validation

            var form1 = $('#form_sample_1');
            var error1 = $('.alert-danger', form1);
            var success1 = $('.alert-success', form1);

            form1.validate({
                errorElement: 'span', //default input error message container
                errorClass: 'help-block help-block-error', // default input error message class
                focusInvalid: false, // do not focus the last invalid input
                ignore: "",  // validate all fields including form hidden input
                messages: {
                    select_multi: {
                        maxlength: jQuery.validator.format("Max {0} items allowed for selection"),
                        minlength: jQuery.validator.format("At least {0} items must be selected")
                    }
                },
                rules: {
                    client_name: {
                        required: true
                    },
                    pet_name: {
                        required: true
                    },
                    email: {
                        required: true,
                        email: true
                    },
                    breed: {
                        required: true
                    },
                    size: {
                        required: true
                    },
                    state: {
                        required: true
                    },
                    zip_code: {
                        required: true
                    },
                    date: {
                        required: true
                    },
                },

                invalidHandler: function (event, validator) { //display error alert on form submit              
                    success1.hide();
                    error1.show();
                    App.scrollTo(error1, -200);
                },

                errorPlacement: function (error, element) { // render error placement for each input type
                    var cont = $(element).parent('.input-group');
                    if (cont) {
                        cont.after(error);
                    } else {
                        element.after(error);
                    }
                },

                highlight: function (element) { // hightlight error inputs

                    $(element)
                        .closest('.form-group').addClass('has-error'); // set error class to the control group
                },

                unhighlight: function (element) { // revert the change done by hightlight
                    $(element)
                        .closest('.form-group').removeClass('has-error'); // set error class to the control group
                },

                success: function (label) {
                    label
                        .closest('.form-group').removeClass('has-error'); // set success class to the control group
                },

                submitHandler: function (form) {
                    success1.show();
                    error1.hide();

                    form[0].submit()
                }
            });


    }

    return {
        //main function to initiate the module
        init: function () {

            handleValidation1();

        }

    };

}();

jQuery(document).ready(function() {
    FormValidation.init();
});
