document.addEventListener('DOMContentLoaded', function () {
    const counters = document.querySelectorAll('.count');
    const speed = 100; // Adjust the speed of counting here

    counters.forEach(counter => {
        const updateCount = () => {
            const target = +counter.getAttribute('data-target');
            const count = +counter.innerText;
            const increment = target / speed;

            if (count < target) {
                counter.innerText = Math.ceil(count + increment);
                setTimeout(updateCount, 20);
            } else {
                counter.innerText = target.toLocaleString();
            }
        };

        // Trigger the counter update when the user scrolls to the section
        const observer = new IntersectionObserver(entries => {
            if (entries[0].isIntersecting) {
                updateCount();
                observer.unobserve(counter);
            }
        }, { threshold: 0.7 });

        observer.observe(counter);
    });
});



document.addEventListener('DOMContentLoaded', function () {
    const donorNameField = document.getElementById('donor_name_field');
    const isAnonymousField = document.getElementById('is_anonymous_field');
    const anonymousWrapper = isAnonymousField.parentNode;

    donorNameField.addEventListener('input', function () {
        if (donorNameField.value.trim() !== '') {
            isAnonymousField.checked = false;
            isAnonymousField.disabled = true;
            anonymousWrapper.classList.add('disabled-checkbox');
        } else {
            isAnonymousField.disabled = false;
            anonymousWrapper.classList.remove('disabled-checkbox');
        }
    });
});


// const scrollContent = document.querySelector('.scroll-content');
//         sampleDonations.forEach(donation => {
//             const div = document.createElement('div');
//             div.className = 'inline-block mx-4 bg-blue-100 rounded-full px-4 py-2 text-blue-800';
//             div.innerHTML = `
//                 <span class="font-bold">${donation.is_anonymous ? 'Anonymous' : donation.donor_name}</span>
//                 donated $${donation.amount} to
//                 <span class="italic">${donation.cause.name}</span>
//             `;
//             scrollContent.appendChild(div);
//         });

const carouselItems = document.querySelectorAll('.carousel-item');
    let currentIndex = 0;

    function showNextSlide() {
        // Hide current slide with fade-out
        carouselItems[currentIndex].classList.replace('opacity-100', 'opacity-0');

        // Move to next slide
        currentIndex = (currentIndex + 1) % carouselItems.length;

        // Show new slide with fade-in
        carouselItems[currentIndex].classList.replace('opacity-0', 'opacity-100');
    }

    // Automatically change slides every 3 seconds
    setInterval(showNextSlide, 4000);


// window.onload = function() {
//     document.getElementById("loader").style.display = "none";
//     document.getElementById("content").style.display = "block";
// };

