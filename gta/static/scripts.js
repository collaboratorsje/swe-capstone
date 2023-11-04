// static/scripts.js

document.addEventListener("DOMContentLoaded", function() {
    setTimeout(function() {
        let alerts = document.querySelectorAll('.alert:not(.static-alert)');
        alerts.forEach(function(alert) {
            alert.style.opacity = '0';
            setTimeout(function() {
                alert.style.display = 'none';
            }, 1000); // Matches the duration of the fade effect
        });
    }, 5000); // Duration until the fade-out starts
});


function togglePasswordVisibility() {
    const passwordField = document.getElementById('passwordField');
    const passwordType = passwordField.getAttribute('type');
    
    if (passwordType === 'password') {
        passwordField.setAttribute('type', 'text');
    } else {
        passwordField.setAttribute('type', 'password');
    }
};

function filterJobs()
{
    let coursef = document.getElementById("course-filter");
    let certf = document.getElementById("cert-filter");
    let rolef = document.getElementById("role-filter");
    let data = JSON.stringify({ "course": coursef.options[coursef.selectedIndex].value, "role": rolef.options[rolef.selectedIndex].value,"cert": certf.checked })
    fetch('/getjobs', {
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        method: "POST",
        body: data
    })
    .then(response => response.json())
    .then(
        data =>
        {
            let jobgroup = document.getElementById("job-list-group");
            let arr = new Array();
            for(c of jobgroup.children) { arr.push(c); };
            for (a of arr) { a.remove(); };
            for (d of Object.entries(data))
            {
                var job = d[1]
                var item = document.createElement('li');
                item.className = "list-group-item";
                var t = document.createElement('h5');
                t.innerHTML = job["course_full"]
                var b = document.createElement('span');
                b.className = "badge badge-primary";
                b.innerHTML = job["role_name"];
                t.appendChild(b);
                var pi = document.createElement('p');
                pi.setAttribute("value", job["course_id"]);
                pi.innerText = "Course ID: " + job["course_id"];
                pi.id = "job-course-id";
                var pc = document.createElement('p');
                if (job["cert"] === true) { pc.innerHTML = "*Requires Certification"} else { pc.innerHTML = "&nbsp;"}
                var sb = document.createElement('a');
                sb.href = "/apply/"+job["job_id"]
                sb.className = "btn apply-btn";
                sb.innerText = "Apply";
                item.appendChild(t);
                item.appendChild(pi);
                item.appendChild(pc);
                item.appendChild(sb);
                jobgroup.appendChild(item);
            }
    })
};
