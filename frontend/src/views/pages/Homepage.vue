<template>
    <div>
        <Card class="w-100">
        <template #content>
                <div class="flex justify-end">
                    <InputGroup class="w-[20rem]">
                        <span class="p-inputgroup-addon">
                            <i class="pi pi-search"></i>
                        </span>
                        <input-text placeholder="Search" class="border border-solid border-slate-400 py-2 px-3"></input-text>
                    </InputGroup>
                </div>
            <data-table class="border rounded mt-5" :value="assistance" selectionMode="single"  paginator :rows="10" :rowsPerPageOptions="[5, 10, 20, 50]" ref="dt">
                <template #header>
                    <div style="text-align: left">
                        <Button icon="pi pi-external-link" class="bg-sky-500 px-5 py-2 text-white" label="Export" @click="exportCSV($event)" />
                    </div>
                </template>
               <Column v-for="header in headers" :key="header.field" :field="header.field" :header="header.header">
                    <template v-if="header.field == 'FullName'" #body="{data}">
                        <span>{{data.FirstName}} {{ data.MiddleName }} {{ data.LastName }}</span>
                    </template>
                    <template v-if="header.field == 'Amount'" #body="{data}">
                        <span v-if="data.Amount == null">N/A</span>
                        <span v-else>₱ {{data.Amount}}</span>
                    </template>
                    <template v-if="header.field == 'actions'" #body="{data}">
                        <Button icon="pi pi-eye" style="color:orange" class="p-button-rounded p-button-info" @click="openClientProcessorDialog(data)"></Button>
                        <Button icon="pi pi-trash" style="color:red" class="p-button-rounded p-button-danger"></Button>
                    </template>
                </Column>
            </data-table>
        </template>
    </Card>
    <ClientProcessorDialog :visible="clientProcessorDialogShow" :client="clientData" :processor="processorData" @close="closeClientProcessorDialog"></ClientProcessorDialog>
    </div>
    
    
</template>

<script>
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import InputText from 'primevue/inputtext';
import Card from 'primevue/card';
import InputGroup from 'primevue/inputgroup';
import InputGroupAddon from 'primevue/inputgroupaddon';
import Button from 'primevue/button';
import { onMounted, ref } from 'vue';
import ClientProcessorDialog from '@/components/dialogs/client-processor-dialog.vue'
import axios from '@axios';
export default {
    components: {
        DataTable,
        Column,
        InputText,
        Card,
        InputGroup,
        InputGroupAddon,
        Button,
        ClientProcessorDialog,
    },
    setup() {
        
        const assistance = ref([])
        const clientData = ref({})
        const processorData = ref({})
        const clientProcessorDialogShow = ref(false)
        const headers = ref([
           
            {field: 'FullName', header: 'Full Name'},
            {field: 'TypeOfAssistance', header: 'Type Of Assistance'},
            {field: 'Category', header: 'Category'},
            {field: 'SourceOfFund', header: 'Source of Fund'},
            {field: 'Amount', header: 'Amount'},
            {field: 'ReceivedDate', header: 'Received Date'},
            {field: 'Mode', header: 'Mode'},
            {field: 'actions', header: 'Actions'}
        ])

        const dt = ref()

        const getData = () => {
            axios.get('get-data')
            .then(response => {
                assistance.value = response.data.data
            })
        }

        const editAssistance = (data) => {
            console.log(data)
        }

        const exportCSV = (event) => {
            dt.value.exportCSV()    
        }

        const openClientProcessorDialog = (client) => {
            axios.get(`get-client-processor-data`, {
                params: {
                    control_number: client.ControlNumber,
                    record_number: client.RecordNumber
                }
            }).then(response => {
                
                clientData.value = {
                    fullName: `${client.FirstName} ${client.MiddleName} ${client.LastName}`,
                    ...response.data.client
                }
  
                processorData.value = response.data.processor
                clientProcessorDialogShow.value = true
            })
        }

        const closeClientProcessorDialog = () => {
            clientProcessorDialogShow.value = false
        }

        onMounted(() => {
           getData()
        })
        return {
            // variables
            headers,
            assistance,
            dt,
            clientProcessorDialogShow,
            clientData,
            processorData,
      
            // methods
            editAssistance,
            exportCSV,
            openClientProcessorDialog,
            closeClientProcessorDialog,

        }
  
    },
}
</script>