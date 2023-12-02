function populateOptions(data) {
    formatFacultyOptions(data.Faculty, 'selectFaculty', 'Add Relation');
    formatCommitteeOptions(data.Committee, 'selectCommittee');

    const facultyList = data.Table.map(row => row.Name);
    const uniqueFacultyList = [...new Set(facultyList)];
    
    formatFacultyOptions(uniqueFacultyList, 'editFaculty', 'Edit Relation');
}

/* Formatting function for row details - modify as you need */
function format(row) {
    return (
        row.Name + ' is on ' + row.Committee.Name + ' until ' + row.Committee.Until + '.'
    );
}

sessionStorage['Group By'] = sessionStorage['Group By'] == undefined ? 'Committee' : sessionStorage['Group By'];

$(document).ready(function () {
    getData('/get/Relation').then((data) => {
        console.log(data);
        populateOptions(data);

        let switchGroup = sessionStorage['Group By'] == 'Committee' ? 'Faculty': 'Committee';

        if (sessionStorage['Group By'] == 'Committee') {
            var table = $('#relationTable').DataTable({
                data: data.Table,
                select: true,
                dom: 'PBfrtip',
                pageLength: 20,
                'order': [[4, 'asc']],
                buttons: [
                    {
                        text: 'Delete Selected Row',
                        action: function () {
                            let rows = table.rows({ selected: true }).data();
                            rows.map(function (row) {
                                row = { 'FacultyName': row['Name'], 'CommitteeCode': row['Committee']['Code'] };
                                sendData('/remove/Relation', row);
                            })
    
                        }
                    },
                    {
                        text: 'Add Relation',
                        action: function () {
                            $('#relationAddModal').modal('show');
                        }
                    },
                    {
                        text: 'Edit Relation',
                        action: function () {
                            $('#relationEditModal').modal('show');
                        }
                    },
                    {
                        text: 'Group by ' + switchGroup,
                        action: function() {
                            sessionStorage['Group By'] = switchGroup;
                            location.reload(true);
                        } 
                    }
                ],
                rowGroup: {
                    dataSrc: 'Committee.Name',
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
                    },
                    { // 1
                        data: 'Attributes',
                        render: {
                            sp: '[].Department',
                            display: '[, ].Department'
                        },
                        searchPanes: {
                            header: 'Department',
                            orthogonal: 'sp',
                        }
                    },
                    { // 2
                        data: 'Attributes',
                        render: {
                            sp: '[].Affiliation',
                            display: '[, ].Affiliation'
                        },
                        searchPanes: {
                            header: 'Affiliation',
                            orthogonal: 'sp'
                        }
                    },
                    { // 3
                        data: 'Attributes',
                        render: {
                            sp: '[].Title',
                            display: '[, ].Title'
                        },
                        searchPanes: {
                            header: 'Title',
                            orthogonal: 'sp'
                        }
                    },
                    { // 4
                        data: 'Committee.Name',
                        'orderData': [4],
                        visible: false
                    },
                    { // 5
                        data: 'Committee.Until',
                    }
                ],
            });
        } else {
            var table = $('#relationTable').DataTable({
                data: data.Table,
                select: true,
                dom: 'PBfrtip',
                pageLength: 20,
                'order': [[0, 'asc']],
                buttons: [
                    {
                        text: 'Delete Selected Row',
                        action: function () {
                            let rows = table.rows({ selected: true }).data();
                            rows.map(function (row) {
                                row = { 'FacultyName': row['Name'], 'CommitteeCode': row['Committee']['Code'] };
                                sendData('/remove/Relation', row);
                            })
    
                        }
                    },
                    {
                        text: 'Add Relation',
                        action: function () {
                            $('#relationAddModal').modal('show');
                        }
                    },
                    {
                        text: 'Edit Relation',
                        action: function () {
                            $('#relationEditModal').modal('show');
                        }
                    },
                    {
                        text: 'Group by ' + switchGroup,
                        action: function() {
                            sessionStorage['Group By'] = switchGroup;
                            location.reload(true);
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
                columnDefs: [
                    {
                        visible: false,
                        target: [0, 1, 2, 3]
                    },
                    {
                        searchPanes: {
                            show: false
                        },
                        target: [1, 2, 3]
                    }
                ],
                columns: [
                    { // 0
                        data: 'Name',
                        'orderData': [0],
                    },
                    { // 1
                        data: 'Attributes',
                        render: {
                            sp: '[].Department',
                            display: '[, ].Department'
                        }
                    },
                    { // 2
                        data: 'Attributes',
                        render: {
                            sp: '[].Affiliation',
                            display: '[, ].Affiliation'
                        }
                    },
                    { // 3
                        data: 'Attributes',
                        render: {
                            sp: '[].Title',
                            display: '[, ].Title'
                        }
                    },
                    { // 4
                        data: 'Committee.Name',
                    },
                    { // 5
                        data: 'Committee.Until',
                    }
                ],
            });
        }

        // Populate Committee Options on Faculty Selection in Editing Relation
        $('#editFaculty').on('change', function() {
            let validRows = data.Table.filter(row => row.Name == $('#editFaculty').val());
            let committeeList = validRows.map(row => ({'Name': row.Committee.Name, 'Code': row.Committee.Code}));
            formatCommitteeOptions(committeeList, 'editCommittee');
        });

        // Handle the 'Save' button click within the modal
        $('#saveRelationAdd').click(function () {
            let obj = {
                'FacultyName': $('#selectFaculty').val(),
                'CommitteeCode': $('#selectCommittee').val(),
                'ServingPeriod': $('#selectServingUntil').val()
            };

            sendData('/add/Relation', obj);
            $('#relationAddModal').modal('hide');
        });

        $('#saveRelationEdit').click(function () {
            let obj = {
                'Lookup Keys': [
                    {'FacultyName': $('#editFaculty').val()},
                    {'CommitteeCode': $('#editCommittee').val()}
                ],
                'Update Key': 'ServingPeriod',
                'Update Value': $('#editServingUntil').val()
            };

            sendData('/edit/Relation', obj);
            $('#relationEditModal').modal('hide');
        });

        // Handle the 'Close' button click within the modal
        $('#closeRelationAdd').click(function () {
            $('#relationAddModal').modal('hide');
        });

        $('#closeRelationEdit').click(function () {
            $('#relationEditModal').modal('hide');
        });

    }).catch((error) => { console.log(error) })
});