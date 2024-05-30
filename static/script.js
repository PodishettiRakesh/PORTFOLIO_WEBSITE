document.addEventListener('DOMContentLoaded', function () {
    var typed = new Typed(".text", {
        strings: ["Frontend Developer", "Full Stack developer", "Web Developer"],
        typeSpeed: 100,
        backSpeed: 100,
        backDelay: 1000,
        loop: true
    });

    document.getElementById('contactForm').addEventListener('submit', function(event) {
        event.preventDefault();

        var formData = new FormData(this);

        fetch('/submit-form', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Message sent successfully!');
            } else {
                alert('Error sending message.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error sending message.');
        });
    });
});


