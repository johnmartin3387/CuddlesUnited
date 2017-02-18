var FormWizard = function () {


    return {
        //main function to initiate the module
        init: function () {  

	    function format(state) {
                if (!state.id) return state.text; // optgroup
                return "<img class='flag' src='/static/global/img/flags/" + state.id.toLowerCase() + ".png'/>&nbsp;&nbsp;" + state.text;
            }
        
            $("#country_list").select2({
                placeholder: "Select",
                allowClear: true,
                formatResult: format,
                width: 'auto', 
                formatSelection: format,
                escapeMarkup: function (m) {
                    return m;
                }
            });

            var form = $('#basic_info_form');
            var error = $('.alert-danger', form);
            var success = $('.alert-success', form);

            form.validate({
                doNotHideMessage: true, //this option enables to show the error/success messages on tab switch.
                errorElement: 'span', //default input error message container
                errorClass: 'help-block help-block-error', // default input error message class
                focusInvalid: false, // do not focus the last invalid input
                rules: {
                    //account
                    //personal info
                    firstname: {
                        required: true
                    },
					lastname: {
                        required: true
                    },
                    phone: {
                        required: true
                    },
                    gender: {
                        required: true
                    },
                    address: {
                        required: true
                    },
                    city: {
                        required: true
                    },
					state: {
                        required: true
                    },
                    country: {
                        required: true
                    },
		            zipcode: {
                        required: true
                    }
                },

                errorPlacement: function (error, element) { // render error placement for each input type
                    if (element.attr("name") == "gender") { // for uniform radio buttons, insert the after the given container
                        error.insertAfter("#form_gender_error");
                    } else if (element.attr("name") == "payment[]") { // for uniform checkboxes, insert the after the given container
                        error.insertAfter("#form_payment_error");
                    } else {
                        error.insertAfter(element); // for other inputs, just perform default behavior
                    }
                },

                invalidHandler: function (event, validator) { //display error alert on form submit   
                    success.hide();
                    error.show();
                    App.scrollTo(error, -200);
                },

                highlight: function (element) { // hightlight error inputs
                    $(element)
                        .closest('.form-group').removeClass('has-success').addClass('has-error'); // set error class to the control group
                },

                unhighlight: function (element) { // revert the change done by hightlight
                    $(element)
                        .closest('.form-group').removeClass('has-error'); // set error class to the control group
                },

                success: function (label) {
                    if (label.attr("for") == "gender" || label.attr("for") == "payment[]") { // for checkboxes and radio buttons, no need to show OK icon
                        label
                            .closest('.form-group').removeClass('has-error').addClass('has-success');
                        label.remove(); // remove error label here
                    } else { // display success icon for other inputs
                        label
                            .addClass('valid') // mark the current input as valid and display OK icon
                        .closest('.form-group').removeClass('has-error').addClass('has-success'); // set success class to the control group
                    }
                },

                submitHandler: function (form) {
                    success.show();
                    error.hide();
                    form[0].submit();
                    //add here some ajax code to submit your form or just call form.submit() if you want to submit the form without ajax
                }

            });  

            $(".basic-save").click(function(){
                var text = $(".zipcode").val()
                $("#static").modal("show")

                GMaps.geocode({
                    address: text,
                    callback: function (results, status) {
                        if (status == 'OK') {
                            var latlng = results[0].geometry.location;

                            $(".lat").val(latlng.lat())
                            $(".lng").val(latlng.lng())
                            document.basic_info_form.submit();

                            /*QB.init(QBApp.appId, QBApp.authKey, QBApp.authSecret, config);

                            var user_token = {
                                email: $(".email").val(),
                                password: $(".password").val() + pass_suffix,
                                full_name: $(".first_name").val() + " " + $(".last_name").val()
                            };

                            QB.init(QBApp.sessionToken, QBApp.appId);
                            QB.createSession(function(err, result) {
                              QB.users.create(user_token, function(err, user){
                                  if (user) {
                                    $(".chat_id").val(user.id)
                                    $("#static").modal("hide")
                                    document.basic_info_form.submit();
                                  }
                                });
                            });*/
                        }
                        else{
                            alert("Failed to fetch geo location.")
                        }
                    }
                });
            })

            form = $('#account_info_form');

            form.validate({
                doNotHideMessage: true, //this option enables to show the error/success messages on tab switch.
                errorElement: 'span', //default input error message container
                errorClass: 'help-block help-block-error', // default input error message class
                focusInvalid: false, // do not focus the last invalid input
                rules: {
                    //profile
		    description:{
			required: true
                    },
                    profile_title: {
                        required: true
                    },
                    profile_rate: {
			digits: true,
                        required: true
                    },
                    /*discount_rate: {
                        digits: true,
                        required: true
                    },
                    discount_hour: {
                        digits: true,
                        required: true
                    }*/
                },

                errorPlacement: function (error, element) { // render error placement for each input type
                    if (element.attr("name") == "gender") { // for uniform radio buttons, insert the after the given container
                        error.insertAfter("#form_gender_error");
                    } else if (element.attr("name") == "payment[]") { // for uniform checkboxes, insert the after the given container
                        error.insertAfter("#form_payment_error");
                    } else {
                        error.insertAfter(element); // for other inputs, just perform default behavior
                    }
                },

                invalidHandler: function (event, validator) { //display error alert on form submit   
                    success.hide();
                    error.show();
                    App.scrollTo(error, -200);
                },

                highlight: function (element) { // hightlight error inputs
                    $(element)
                        .closest('.form-group').removeClass('has-success').addClass('has-error'); // set error class to the control group
                },

                unhighlight: function (element) { // revert the change done by hightlight
                    $(element)
                        .closest('.form-group').removeClass('has-error'); // set error class to the control group
                },

                success: function (label) {
                    if (label.attr("for") == "gender" || label.attr("for") == "payment[]") { // for checkboxes and radio buttons, no need to show OK icon
                        label
                            .closest('.form-group').removeClass('has-error').addClass('has-success');
                        label.remove(); // remove error label here
                    } else { // display success icon for other inputs
                        label
                            .addClass('valid') // mark the current input as valid and display OK icon
                        .closest('.form-group').removeClass('has-error').addClass('has-success'); // set success class to the control group
                    }
                },

                submitHandler: function (form) {
                    success.show();
                    error.hide();
                    form[0].submit();
                    //add here some ajax code to submit your form or just call form.submit() if you want to submit the form without ajax
                }

            });          

            //apply validation on select2 dropdown value change, this only needed for chosen dropdown integration.
            $('#country_list', form).change(function () {
                form.validate().element($(this)); //revalidate the chosen dropdown value and show error or success message for the input
            });
        }

    };

}();

jQuery(document).ready(function() {
    FormWizard.init();
});
