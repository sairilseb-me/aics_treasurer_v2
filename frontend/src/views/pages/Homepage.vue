<template>
    <Card class="w-100">
        <template #content>
                <div class="flex justify-end">
                    <Button class="border border-solid border-slate-500 bg-sky-600 py-2 px-3 text-white" @click="test_connect">
                        <i class="pi pi-file"></i>
                        <span class="ml-2">Export  to Excel</span>
                    </Button>
                    <InputGroup class="w-[20rem]">
                        <span class="p-inputgroup-addon">
                            <i class="pi pi-search"></i>
                        </span>
                        <input-text placeholder="Search" class="border border-solid border-slate-400 py-2 px-3"></input-text>
                    </InputGroup>
                </div>
            <data-table class="border rounded mt-5">
               <Column v-for="header in headers" :key="header.field" :field="header.field" :header="header.header"></Column>
            </data-table>
        </template>
    </Card>
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
    },
    setup() {
        
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

        const test_connect = () => {
            axios.get('test')
            .then(response => {
                console.log(response)
            })
        }

        onMounted(() => {
            console.log(import.meta.env.VITE_API_URL)
        })
        return {
            // variables
            headers,

            // methods
            test_connect,

        }
  
    },
}
</script>