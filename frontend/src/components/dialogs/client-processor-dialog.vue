<template>
    <Dialog v-model:visible="visible" modal header="Client's Assistance Data" :style="{ width: '50rem'}" @hide="closeDialog">
        
        <Panel class="border border-solid border-slate-800">
            <template #header>
                <div class="flex items-center gap-2 justify-between w-full">
                    <h2 class="text-xl"><strong>Patient Data</strong></h2>
                    <h4 class="text-xl"><strong>Amount to be released:</strong> ₱ {{ formatCurrency(clientData.Amount) }}</h4>
                </div>
            </template>
            <p><strong>Name:</strong> {{ client.fullName }}</p>
            <p><strong>Address:</strong> {{ client.address }}</p>
            <p><strong>Control Number:</strong> {{ clientData.ControlNumber }}</p>
            <p><strong>Record Number:</strong> {{ clientData.RecordNumber }}</p>
            <p><strong>Type Of Assistance:</strong> {{ clientData.TypeOfAssistance }}</p>
            <p><strong>Category:</strong> {{ clientData.Category }}</p>
            <p><strong>Source of Fund:</strong> {{ clientData.SourceOfFund }}</p>
            <p><strong>Budget Balance:</strong> ₱ {{ formatCurrency(budget_balance) }}</p>
        </Panel>
        <Panel class="border border-solid border-slate-800 mt-3">
            <template #header>
                <div class="flex items-center gap-2">
                    <h2 class="text-xl"><strong>Processor Data</strong></h2>
                </div>
            </template>
            <p><strong>Name:</strong> {{ processorData.FirstName }} {{ processorData.MiddleName }} {{ processorData.LastName }}</p>
            <p><strong>ID Presented:</strong> {{ processorData.IDPresented }}</p>
            <p><strong>ID Number:</strong> {{ processorData.IDNumber }}</p>
            <p><strong>Relationship with Client:</strong> {{ processorData.Relationship }}</p>
        </Panel>
        <FloatLabel class="mt-5">
                <Textarea v-model="comment" rows="5" cols="30" class="w-full border border-slate-700 p-3" />
                <label>Comment</label>
            </FloatLabel>
        <template #footer>
            <div v-if="!loading" class="flex justify-between w-full">
                <div>
                    <Button type="button" label="Cancel" severity="secondary" class="border border-solid border-slate-400 bg-slate-500 text-white px-5 py-2 mr-3" @click="closeDialog"></Button>
                    <Button type="button" label="Save" class="border border-solid border-slate-400 bg-green-500 text-white px-5 py-2" @click="save"></Button>
                </div>
                <Button type="button" label="Release" class="border border-solid border-slate-400 bg-blue-500 text-white px-5 py-2" @click="release"></Button>
            </div>
        </template>
    </Dialog>
</template>

<script>
import Dialog from 'primevue/dialog';
import Panel from 'primevue/panel';
import Card from 'primevue/card';
import Textarea from 'primevue/textarea';
import ToastService from '@/plugins/toasts'
import { watch, ref } from 'vue';
import axios from '@axios'
export default {
    components: {
        Dialog,
        Card,
        Panel,
        Textarea,
    },
    props: {
        visible: {
            type: Boolean,
            default: false
        },
        client: {
            type: Object,
            default: {}
        },
        processor: {
            type: Object,
            default: {}
        },
        balance: {
            type: Number,
            default: 0
        }
    },
    setup(props, { emit }) {
        
        const visible = ref(false)
        const clientData = ref({})
        const processorData = ref({})
        const budget_balance = ref(0)
        const comment = ref('')
        const toast = new ToastService()
        const loading = ref(false)

        watch(
            () => props.visible,
            (value) => {
                visible.value = value
            }
        )

        watch(
            () => props.client,
            (value) => {
                if (value.ControlNumber) {
                    clientData.value = value
                    processorData.value = props.processor
                    budget_balance.value = props.balance
                }
            }
        )

        const formatCurrency = (value) => {
            return value.toLocaleString()
        }

        const save = () => {
            loading.value = true
            if (comment.value) {
                const final_comment = `${clientData.value.ProblemPresented} \n Treasurer's Comment: ${comment.value}`
                axios.post(`/save-comment/${clientData.value.ControlNumber}/${clientData.value.RecordNumber}`, {
                    comment: final_comment,
                }).then(response => {
                    if (response.data.success) {
                        toast.showMessage('success', 'Success', 'Comment has been saved.')
                        comment.value = ''
                    }else {
                        toast.showMessage('error', 'Error', 'An error occured while saving comment. Please try again.')
                    }
                }).catch(error => {
                    toast.showMessage('error', 'Error', 'Cannot connect to server. Please try again.')
                }).finally(() => {
                loading.value = false
            })
                
            }
            closeDialog()
        }

        const release = () => {
            if (clientData.value.Amount > budget_balance.value) {
                toast.showMessage('error', 'Error', 'Insufficient budget balance.')
                return
            }
            axios.post(`release-assistance/${clientData.value.ControlNumber}/${clientData.value.RecordNumber}/${clientData.value.SourceOfFund}/${localStorage.getItem('username')}`)
            .then(response => {
                if (response.status == 200){
                    toast.showMessage('success', 'Success', 'Assistance has been released.')
                    closeDialog()
                } else {
                    toast.showMessage('error', 'Error', 'An error occured while releasing assistance. Please try again.')
                }
            }).catch(error => {
                if (error.response){
                    if (error.response.status == 500){
                        toast.showMessage('error', 'Error', 'Cannot connect to server. Please try again.')
                    }
                }
            })
        }

        const closeDialog = () => {
            emit('close')
            resetValues()
        }

        const resetValues = () => {
            clientData.value = {}
            processorData.value = {}
            budget_balance.value = 0
        }


        return {
            //variable
            visible,
            clientData,
            processorData,
            comment,
            budget_balance,
            loading,

            //methods
            closeDialog,
            save,
            formatCurrency,
            release,
        }
    },
}
</script>