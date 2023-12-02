$(document).ready(function () {
    getData('/get/Faculty').then((data) => {
        console.log(data);
        formatFacultyOptions(data.Faculty, 'selectFaculty', 'Edit Faculty');

        var table = $('#facultyTable').DataTable({
            data: data.Table,
            select: true,
            dom: 'PBfrtip',
            pageLength: 20,
            "order": [[0, 'asc']],
            buttons: [
                {
                    text: "Delete Selected Row",
                    action: function () {
                        let rows = table.rows({ selected: true }).data();
                        rows.map(function(row) {
                            row = {'FacultyName': row['Name'], 'FacultyDepartment': row['Department']};
                            sendData('/remove/Faculty', row);
                        })

                    }
                },
                {
                    text: "Add Faculty",
                    action: function () {
                        $('#facultyAddModal').modal('show');
                    }
                },
                {
                    text: "Edit Faculty",
                    action: function () {
                        $('#facultyEditModal').modal('show');
                    }
                }
            ],
            rowGroup: {
                dataSrc: 'Name',
                startRender: function(rows, group) {
                    var style = '"background-color: rgb(209, 209, 209);"';
                    var td = '<td style=' + style + ' colspan=5>' + group + '</td>';
                    return $('<tr class="group group-start">' +  td + '</tr>');
                }
            },
            searchPanes: {
                cascadePanes: true,
                threshold: 1.0,
            },
            columns: [
                { // 0
                    data: 'Name',
                    "orderData": [0],
                    visible: false,
                },
                { // 1
                    data: 'Department',
                },
                { // 2
                    data: 'Affiliation',
                },
                { // 3
                    data: 'Title',

                }
            ],
        });
        
        // Edit functionality
        $('#selectFacultyChangeKey').on('change', function() {
            let lookup_value = $('#selectFaculty').val().split(' | ');
            let faculty = data.Table.find(item => item.Name == lookup_value[0] && item.Department == lookup_value[1]);
            let key = $('#selectFacultyChangeKey option:selected').text();

            $('#currentFacultyValue').attr('placeholder', faculty[key]);
        });

        // Handle the "Save" button click within the modal
        $('#saveFacultyAdd').click(function () {
            let obj = {
                'FacultyName': $('#facultyName').val(),
                'FacultyDepartment': $('#facultyDepartment').val(),
                'FacultyAffiliation': $('#facultyAffiliation').val(),
                'FacultyTitle': $('#facultyTitle').val()
            };

            sendData("/add/Faculty", obj);
            $('#facultyAddModal').modal('hide');
        });

        $('#saveFacultyEdit').click(function () {
            let lookup_value = $('#selectFaculty').val().split(' | ');
            let key = $('#selectFacultyChangeKey').val();
            let value = $('#newFacultyValue').val();

            let obj = {
                'Lookup Keys': [
                    {"FacultyName": lookup_value[0], "FacultyDepartment": lookup_value[1]}
                ],
                'Update Key': key,
                'Update Value': value
            };

            sendData("/edit/Faculty", obj);
            $('#facultyEditModal').modal('hide');
        });
        
        // Handle the "Close" button click within the modal
        $('#closeFacultyAdd').click(function () {
            $('#facultyAddModal').modal('hide');
        });

        $('#closeFacultyEdit').click(function () {
            $('#facultyEditModal').modal('hide');
        });

    }).catch((error) => { console.log(error) })
});