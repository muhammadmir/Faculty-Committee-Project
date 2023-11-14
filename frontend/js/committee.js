$(document).ready(function () {
    getData('/get/Committee').then((data) => {
        console.log(data);
        formatCommitteeOptions(data.Committee, 'selectCommittee');

        var table = $('#committeeTable').DataTable({
            data: data.Table,
            select: true,
            dom: 'PBfrtip',
            buttons: [
                {
                    text: "Delete Selected Row",
                    action: function () {
                        let rows = table.rows({ selected: true }).data();
                        rows.map(function(row) {
                            row = {'CommitteeName': row['Name']};
                            sendData('/remove/Committee', row);
                        })

                    }
                },
                {
                    text: "Add Committee",
                    action: function () {
                        $('#committeeAddModal').modal('show');
                    }
                },
                {
                    text: "Edit Committee",
                    action: function () {
                        $('#committeeEditModal').modal('show');
                    }
                }
            ],
            searchPanes: {
                cascadePanes: true,
                threshold: 1.0,
            },
            columnDefs: [
                {
                    searchPanes: {
                        show: false
                    },
                    target: [0, 1]
                }
            ],
            columns: [
                { // 0
                    data: 'Code',
                },
                { // 1
                    data: 'Name',
                },
                { // 2
                    data: 'Type',
                },
                { // 3
                    data: 'Designation',

                }
            ],
        });

        // Edit functionality
        $('#selectCommitteeChangeKey').on('change', function() {
            let committee = data.Table.find(item => item.Code == $('#selectCommittee').val());
            let key = $('#selectCommitteeChangeKey option:selected').text();

            $('#currentCommitteeValue').attr('placeholder', committee[key]);
        });

        // Handle the "Save" button click within the modal
        $('#saveCommitteeAdd').click(function () {
            let obj = {
                'CommitteeDesignation': $('#committeeDesignation').val(),
                'CommitteeCode': $('#committeeCode').val(),
                'CommitteeName': $('#committeeName').val(),
                'CommitteeType': $('#committeeType').val()
            };

            sendData("/add/Committee", obj);
            $('#committeeAddModal').modal('hide');
        });

        $('#saveCommitteeEdit').click(function () {
            let lookup_value = $('#selectCommittee').val();
            let key = $('#selectCommitteeChangeKey').val();
            let value = $('#newCommitteeValue').val();

            let obj = {
                'Lookup Keys': [
                    {"CommitteeCode": lookup_value}
                ],
                'Update Key': key,
                'Update Value': value
            };

            sendData("/edit/Committee", obj);
            $('#committeeEditModal').modal('hide');
        });
        
        // Handle the "Close" button click within the modal
        $('#closeCommitteeAdd').click(function () {
            $('#committeeAddModal').modal('hide');
        });

        $('#closeCommitteeEdit').click(function () {
            $('#committeeEditModal').modal('hide');
        });

    }).catch((error) => { console.log(error) })
});