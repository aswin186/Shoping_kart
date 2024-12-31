function editProfile() {
    // Enable input fields for editing
    document.getElementById("name").disabled = false;
    document.getElementById("email").disabled = false;
    document.getElementById("phone").disabled = false;

    // Show "Verify Phone" button
    // document.getElementById("verifyPhone").style.display = "block";
    // document.getElementById("verifyEmail").style.display = "block";

    // Hide Edit button, show Update button
    document.getElementById("editBtn").style.display = "none";
    document.getElementById("updateBtn").style.display = "inline-block";
}

// function verifyPhone() {
//     const phone = document.getElementById("phone").value;
//     // Add your phone verification logic here
//     alert("Phone verification process started for: " + phone);
// }

// function verifyEmail() {
//     const email = document.getElementById("email").value;
//
//     alert("Email verification process started for: " + email);
// }

document.getElementById('email').addEventListener('change', function() {
        // document.getElementById('categoryForm').submit();
    const email = document.getElementById("email").value;

    alert("Email verification process started for: " + email);
    });

function editAddress() {
    // Enable address fields for editing
    document.getElementById("street").disabled = false;
    document.getElementById("city").disabled = false;
    document.getElementById("district").disabled = false;
    document.getElementById("state").disabled = false;
    document.getElementById("landmark").disabled = false;
    document.getElementById("pincode").disabled = false;
    document.getElementById("country").disabled = false;

    // Hide Edit button, show Update button
    document.getElementById("editAddressBtn").style.display = "none";
    document.getElementById("updateAddressBtn").style.display = "inline-block";
}
