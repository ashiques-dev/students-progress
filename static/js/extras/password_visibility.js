$(document).ready((()=>{const $togglePasswordButton=$("#toggle_password_visibility");const $checkIcon=$("#checkIcon");const $passwordVisibility=$("#password_visibility");const $password=$("#password");const $confirmPassword=$("#confirm_password");$togglePasswordButton.on("click",(()=>{const isPasswordVisible=$password.attr("type")==="password";const newType=isPasswordVisible?"text":"password";$password.attr("type",newType);$confirmPassword.attr("type",newType);if(isPasswordVisible){$checkIcon.addClass("bg-gradient-to-t from-stone-600 to-stone-950 text-white").html('<svg class="size-4" stroke-width="2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M5 12l5 5L20 7"></path></svg> ');$passwordVisibility.text("Hide Password")}else{$checkIcon.removeClass("bg-gradient-to-t from-stone-600 to-stone-950 text-white").empty();$passwordVisibility.text("Show password")}}))}));