// static/scripts.js

document.addEventListener("DOMContentLoaded", function() {

    // Fade out alerts
    setTimeout(function() {
        let alerts = document.querySelectorAll('.alert:not(.static-alert)');
        alerts.forEach(function(alert) {
            alert.style.opacity = '0';
            setTimeout(function() {
                alert.style.display = 'none';
            }, 1000); // Matches the duration of the fade effect
        });
    }, 5000); // Duration until the fade-out starts

    // Toggle GTA certification logic
    var checkbox = document.getElementById('toggleGtaCert');
    if (checkbox) {
        var gtaCertField = document.querySelector('.gta-cert-field');
        if (gtaCertField) {
            gtaCertField.style.display = checkbox.checked ? 'block' : 'none';
            checkbox.addEventListener('change', function() {
                gtaCertField.style.display = checkbox.checked ? 'block' : 'none';
            });
        }
    }

    // Add event listener for search form submission
    var searchForm = document.getElementById('search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', function(event) {
            event.preventDefault(); // Prevent the form from submitting traditionally
            const searchQuery = document.querySelector('input[name="query"]').value;
            const filteredJobs = searchJobs(searchQuery);
            displaySearchedJobs(filteredJobs);
        });
    }

    loadTabState();
    setupSearchFormListener();
    setupInputEventListener();

    // Call updateJobListingsTitle initially and whenever jobs change
    updateJobListingsTitle();

});

// Define the loadTabState function
function loadTabState() {
    var currentTab = localStorage.getItem('currentTab');
    if (currentTab) {
        if (currentTab === 'jobs') {
            displayJobs();
        } else if (currentTab === 'applications') {
            displayApplications();
        } else if (currentTab === 'users') {
            displayUsers();
        }
    }
}

function togglePasswordVisibility() {
    const passwordField = document.getElementById('passwordField');
    const passwordType = passwordField.getAttribute('type');
    
    if (passwordType === 'password') {
        passwordField.setAttribute('type', 'text');
    } else {
        passwordField.setAttribute('type', 'password');
    }
};

function updateJobListingsTitle() {
    var titleElement = document.getElementById("job-list-title");
    if (titleElement) {
        var jobCount = document.querySelectorAll(".list-group-item").length;
        titleElement.innerText = "Job Listings (" + jobCount + ")";
    }
}

// Call the function initially and whenever jobs change (e.g., filtering)
updateJobListingsTitle();

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
                if (job["cert"] === true) { pc.innerHTML = '<span class="badge badge-primary">Certification Required</span>'} else { pc.innerHTML = "&nbsp;"}
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
            updateJobListingsTitle();
    })
};

function searchJobs(query) {
    const lowerCaseQuery = query.toLowerCase();

    // If the query is empty, return the full jobs array
    if (!query.trim()) {
        return jobs;
    }

    // Adjust the condition to match the course name or job title
    return jobs.filter(job =>
        job[0].toLowerCase().includes(lowerCaseQuery) || // course name
        job[2].toLowerCase().includes(lowerCaseQuery) || // job title
        job[3].toLowerCase().includes(lowerCaseQuery)
    );
}

function displaySearchedJobs(filteredJobs) {
    const jobListElement = document.getElementById('job-list-group');
    jobListElement.innerHTML = ''; // Clear current job listings

    filteredJobs.forEach(job => {
        const jobItem = document.createElement('li');
        jobItem.className = 'list-group-item';
        jobItem.innerHTML = `
            <h5>${job[0]} - ${job[3]} <span class="badge badge-primary">${job[2]}</span></h5>
            <p>Course ID: ${job[4]}</p>
            ${job[1] ? '<p><span class="badge badge-primary">Certification Required</span></p>' : '<p>&nbsp;</p>'}
            <a href="/apply/${job[4]}" class="btn apply-btn">Apply</a>
        `;
        jobListElement.appendChild(jobItem);
    });
}

function setupSearchFormListener() {
    var searchForm = document.getElementById('search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', function(event) {
            event.preventDefault(); // Prevent the form from submitting traditionally
            const searchQuery = document.querySelector('input[name="query"]').value;
            const filteredJobs = searchJobs(searchQuery);
            displaySearchedJobs(filteredJobs);
        });
    }
}

function setupInputEventListener() {
    var searchInput = document.querySelector('input[name="query"]');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchQuery = this.value;
            const filteredJobs = searchJobs(searchQuery);
            displaySearchedJobs(filteredJobs);
        });
    }
}


function displayJobs() {
    var x = document.getElementById("jobsList");
    var y = document.getElementById("applicationsList");
    var z = document.getElementById("usersList");
    if (x.style.display === "none") {
        x.style.display = "block";
    }
    y.style.display = "none";
    z.style.display = "none";

    var a = document.getElementById("jobsButton");
    var b = document.getElementById("applicationsButton");
    var c = document.getElementById("usersButton");

    a.classList.add('active');
    b.classList.remove('active');
    c.classList.remove('active');
    saveCurrentTab('jobs');
}

function displayApplications() {
    var x = document.getElementById("applicationsList");
    var y = document.getElementById("jobsList");
    var z = document.getElementById("usersList");
    if (x.style.display === "none") {
        x.style.display = "block";
    }
    y.style.display = "none";
    z.style.display = "none";

    var a = document.getElementById("applicationsButton");
    var b = document.getElementById("jobsButton");
    var c = document.getElementById("usersButton");

    a.classList.add("active");
    b.classList.remove("active");
    c.classList.remove("active");
    saveCurrentTab('applications');
}

function displayUsers() {
    var x = document.getElementById("usersList");
    var y = document.getElementById("jobsList");
    var z = document.getElementById("applicationsList");
    if (x.style.display === "none") {
        x.style.display = "block";
    }
    y.style.display = "none";
    z.style.display = "none";

    var a = document.getElementById("usersButton");
    var b = document.getElementById("jobsButton");
    var c = document.getElementById("applicationsButton");

    a.classList.add("active");
    b.classList.remove("active");
    c.classList.remove("active");
    saveCurrentTab('users');
}

function confirmAndRemoveJob(jobId) {
    if (confirm('Are you sure you want to remove this job?')) {
        fetch('/delete-job', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ jobId: jobId })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Remove the job element from the list or refresh the page
                alert('Job removed successfully');
                window.location.reload(); // Simple way to refresh the page
            } else {
                alert('Error removing job');
            }
        })
        .catch(error => console.error('Error:', error));
    }
}

function confirmAndRemoveApplication(appId) {
    if (confirm('Are you sure you want to reject this application?')) {
        fetch('/reject-application', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({appId: appId})
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const applicationElement = document.getElementById(`application-item-${appId}`);
                if (applicationElement) {
                    applicationElement.remove();
                }
                alert('Application removed successfully');
                // window.location.reload();
            } else {
                alert('Error removing application');
            }
        })
        .catch(error => console.error('Error:', error));
    }
}

function confirmAndAcceptApplication(appId) {
    if (confirm('Are you sure you want to accept this application?')) {
        fetch('/accept-application', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ appId: appId })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success && data.status) { // Check if the application is accepted
                var applicationElement = document.getElementById(`application-item-${appId}`);
                if (applicationElement) {
                    applicationElement.classList.add('accepted-application');
                } else {
                    console.log("No element found with ID: application-item-" + appId);
                }
                alert('Application accepted successfully');
            } else {
                alert('Error accepting application');
            }
        })
        .catch(error => console.error('Error:', error));
    }
}

//{{ url_for('form.EditApplication', job_id=loop.index|string) }}
function openCloseApplicationEditing(appId){
    fetch('/update-open-close', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ appId: appId})
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Remove the application element from the list or refresh the page
            alert('Application editing updated successfully');
            window.location.reload();
        } else {
            alert('Error accepting application');
        }
    })
    .catch(error => console.error('Error:', error));
}

function saveCurrentTab(tabName) {
    localStorage.setItem('currentTab', tabName);
}

function loadTabState() {
    var currentTab = localStorage.getItem('currentTab');
    switch (currentTab) {
        case 'jobs':
            displayJobs();
            break;
        case 'applications':
            displayApplications();
            break;
        case 'users':
            displayUsers();
            break;
        default:
            displayJobs(); // Default to jobs if nothing is saved
            break;
    }
}

function removeUserCourse(courseId) {
    var uc = document.getElementById("ucourses");
    console.log(uc.value);
    var courses = uc.value.split("|");
    console.log(courses);
    let out = "";
    for(c of courses)
    {
        if( !c.startsWith(courseId) && c != "")
        {
            out = out.concat(c, "|");
            console.log("Inloop, Out", out);
        };
    };
    uc.value = out 
    document.getElementById("course-post-" + courseId).outerHTML = "";
};