<template>
    <div>
        <Card>
            <template #header>
                <h2 class="text-3xl pl-5 pt-5">Released Assistance</h2>
            </template>
            <template #content>
                <div class="flex flex-col">
                    <div class="flex justify-end">
                        <div class="flex align-middle">
                            <div class="flex align-middle mr-3">
                                <input type="checkbox" class="border border-solid border-slate-500" id="enableDateFilter" v-model="enableDateFilter" @click="enableDateFilter = !enableDateFilter"/>
                                <label for="enableDateFilter" class="ml-2"> Enable Date Filter </label>
                            </div>
                            <FloatLabel class="mr-3">
                                <Calendar inputId="from" v-model="date_from" :disabled="!enableDateFilter" variant="filled" inputClass="custom-input" class="border border-solid border-slate-400 rounded" />
                                <label for="from">From</label>
                            </FloatLabel>
                            <FloatLabel>
                                <Calendar inputId="to" v-model="date_to" :disabled="!enableDateFilter" variant="filled" class="border border-solid border-slate-400 rounded"/>
                                <label for="to">To</label>
                            </FloatLabel>
                        </div>
                    </div>
                    <div class="flex justify-end align-middle mt-3">
                        <div class="flex mr-3">
                            <input id="checkboxDept" type="checkbox" class="border border-solid border-slate-500 mr-2" v-model="enableDropDown" @click="enableDropDown = !enableDropDown" />
                            <label for="checkboxDept" class="flex items-center">Department: </label>
                        </div>
                        <div>
                           <Dropdown v-model="selectedDept" :disabled="!enableDropDown" :options="departments" optionLabel="name" placeholder="Select a Budget" class="w-14rem"></Dropdown>
                        </div>
                    </div>
                    <div class="flex justify-between mt-3">
                        <InputGroup class="w-[20rem]">
                            <span class="p-inputgroup-addon">
                                <i class="pi pi-search"></i>
                            </span>
                            <input-text placeholder="Search" class="border border-solid border-slate-400 py-2 px-3" @keydown="disableFilters" v-model="search" @change="getReleasedAssistanceData"></input-text>
                        </InputGroup>
                        <Button class="border border-solid border-slate-400 bg-blue-800 text-white px-5 py-2" @click="getReleasedAssistances">Filter</Button>
                    </div>
                    
                <div class="border border-solid border-slate-400 mt-5 pt-3">
                    <DataTable :value="releasedData" selectionMode paginator :rows="10" :loading="tableLoading" :rowsPerPageOptions="[5, 10, 20, 50]">
                        <template #header>
                                <div>
                                    <Button :disabled="disableExport" class="border border-solid border-slate-500 px-5 bg-sky-700 text-white py-2" @click="exportReleasedAssistances">Export<i class="pi pi-arrow-up-right ml-2"></i></Button>
                                </div>
                        </template>
                        <Column v-for="header in releasedColumns" :key="header.field" :field="header.field" :header="header.header">
                            
                            <template v-if="header.field == 'FullName'" #body="{data}">
                                {{data.FirstName}} {{ data.MiddleName }} {{ data.LastName }}
                            </template>
                            <template v-if="header.field == 'Address'" #body="{data}">
                                {{ data.Barangay }} {{ data.Municipality }} {{ data.Province }}
                            </template>
                            <template v-if="header.field == 'Amount'" #body="{data}">
                                <span v-if="data.Amount">₱ {{data.Amount}}</span>
                            </template>
                        </Column>
                    </DataTable>
                </div>
                </div>
            </template>
        </Card>
    </div>
</template>

<script>
import {computed, ref, watch} from 'vue'
import Checkbox from 'primevue/checkbox';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import axios from '@axios';
import ToastService from '@/plugins/toasts';
export default {
    components: {
       Checkbox,
       DataTable,
       Column,
    },
    setup() {

        const enableDateFilter = ref(false);
        const enableDropDown = ref(false);
        const releasedData = ref([]) 
        const selectedDept = ref(null)
        const date_from = ref(null)
        const date_to = ref(null)
        const toast = new ToastService()
        const search = ref('')
        const tableLoading = ref(false)
        const departments = ref([
           {
                name: 'Governors Office',
                value: 'Governors Office'
           },
           {
                name: 'PDF',
                value: 'PDF'
           },
           {
                name: 'PSWDO',
                value: 'PSWDO'
           }
        ])

        const releasedColumns = ref([
            {
                field: 'FullName',
                header: 'Full Name'
            },
            {
                field: 'Address',
                header: 'Address'
            },
            {
                field: 'TypeOfAssistance',
                header: 'Type Of Assistance'
            },
            {
                field: 'SourceOfFund',
                header: 'Source of Fund'
            },
            {
                field: 'Amount',
                header: 'Amount'
            },
            {
                field: 'Mode',
                header: 'Mode'
            },
            {
                field: 'DateRelease',
                header: 'Date Release'
            }
        ])

        watch(
            () => enableDateFilter.value,
            (value) => {
                if (!value){
                    date_from.value = null
                    date_to.value = null
                }
            }
        )

        watch(
            () => enableDropDown.value,
            (value) => {
                if (!value){
                    selectedDept.value = null
                }
            }
        )

        const getReleasedAssistances = () => {

            tableLoading.value = true
            let url = 'get-released-assistances'

            axios.get(url, {
                params: {
                    date_from: date_from.value,
                    date_to: date_to.value,
                    department: selectedDept.value ? selectedDept.value.value : null
                }
            }).then(response => {
                releasedData.value = response.data.data
            }).catch(error => {
                if (error.response.status == 400){
                    toast.showMessage('error', 'Error', 'Make sure that both Date From and Date To are selected.')
                    return
                }
                toast.showMessage('error', 'Error', 'Cannot connect to server. Please try again.')
            }).finally(() => {
                tableLoading.value = false
            })
        }

        const getReleasedAssistanceData = () => {

            let searchParams = {}
            if (search.value.includes(',')) {
                let searchArray = search.value.split(',')
                searchParams = {
                    last_name: searchArray[0].trim(),
                    first_name: searchArray[1].trim()
                }
            } else {
                searchParams = {
                    last_name: search.value.trim()
                }
            }

            axios.get('get-released-assistance', {
                params: searchParams
            })
            .then(response => {
                releasedData.value = response.data.data
            }).catch(error => {
                toast.showMessage('error', 'Error', 'Cannot connect to server. Please try again.')
            }).finally(() => {
                tableLoading.value = false
            })
        }


        const disableExport = computed(() => {
            if (enableDateFilter.value == true && search.value == ''){
                return false
            }

            return true
        })

        const exportReleasedAssistances = async() => {
            let url = 'export-released-assistances'
            await axios.get(url, {
                params: {
                    date_from: date_from.value,
                    date_to: date_to.value,
                    department: selectedDept.value ? selectedDept.value.value : null
                },
                responseType: 'blob',
            }).then(response => {
                if (response.status == 200) {
                    const url = window.URL.createObjectURL(new Blob([response.data]))
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = `${date_from.value}-${date_to.value}-released-assistances.csv`;
                    document.body.appendChild(a);
                    a.click();
                    a.remove();
                    window.URL.revokeObjectURL(url);
                    toast.showMessage('success', 'Success', 'Data has been exported.')
                }
            }).catch(error => {
                console.log(error.response.status)
                if (error.response.status == 400) {
                    toast.showMessage('error', 'Error', 'Make sure that both Date From and Date To are selected.')
                    return
                }
                
                toast.showMessage('error', 'Error', `Cannot connect to server. Please try again.}`)
            })
        } 

        const disableFilters = () => {
            enableDateFilter.value = false
            enableDropDown.value = false
        }

        getReleasedAssistances()

        const resetValues = () => {
            date_from.value = null
            date_to.value = null
            selectedDept.value = null
            search.value = ''
        }

        return {

            //variables
            enableDateFilter,
            enableDropDown,
            departments,
            selectedDept,
            releasedColumns,
            date_from,
            date_to,
            releasedData,
            search,
            tableLoading,

            //computed
            disableExport,

            //methods
            getReleasedAssistances,
            getReleasedAssistanceData,
            disableFilters,
            exportReleasedAssistances,

        }
    }
}
</script>

<style scoped>
    .custom-input {
        padding: 2px 5px 2px 5px !important;
        line-height: 2rem !important;
    }
</style>