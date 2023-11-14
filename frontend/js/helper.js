const sleep = ms => new Promise(r => setTimeout(r, ms));

async function sendData(endpoint, data) {
    try {
        console.log(endpoint);
        console.log(data);
        const response = await fetch("http://127.0.0.1:5000" + endpoint, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        await response.json();
        location.reload(true);
    } catch (error) {
        console.log("Error:", error);
        alert("There was an error sending the data to the server. Please try again.")
        sleep(5000);
        location.reload(true);
    }
}

async function getData(endpoint) {
    try {
        const response = await fetch("http://127.0.0.1:5000" + endpoint, {
            method: "GET",
            headers: {
                "Accept": "application/json"
            }
        });

        const result = await response.json();
        return result['Success'] ? result : false;
    } catch (error) {
        console.log("Error:", error);
        return false;
    }
}

function formatFacultyOptions(facultyList, elementID, location) {
    let selectFaculty = document.getElementById(elementID);
    
    if (location == "Edit Faculty") {
        facultyList.forEach(faculty => {
            let facultyOption = document.createElement('option');
            facultyOption.value = faculty.Name + " | " + faculty.Department;
            facultyOption.text = faculty.Name + " | " + faculty.Department;
            selectFaculty.appendChild(facultyOption);
        })
    } else if (location.includes("Relation")) {
        let uniqueFacultyList = facultyList;
        if (location == "Add Relation") {
            const facultyNames = facultyList.map(faculty => faculty.Name);
            uniqueFacultyList = [...new Set(facultyNames)]; // There's a problem with string encoding, needs to be checked beforehand.
        }
        
        uniqueFacultyList.forEach(facultyName => {
            let facultyOption = document.createElement('option');
            facultyOption.value = facultyName;
            facultyOption.text = facultyName;
            selectFaculty.appendChild(facultyOption);
        })
    }
    
}

function formatCommitteeOptions(committeeList, elementID) {
    let selectCommittee = document.getElementById(elementID);
    committeeList.forEach(committee => {
        let committeeOption = document.createElement('option');
        committeeOption.value = committee.Code;
        committeeOption.text = committee.Code + " | " + committee.Name;
        selectCommittee.appendChild(committeeOption);
    })
}