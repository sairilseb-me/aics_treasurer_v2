<script setup>
import { useLayout } from '@/layout/composables/layout';
import { ref, computed } from 'vue';
import axios from '@axios'

const { layoutConfig } = useLayout();
const username = ref('');
const usernameRef = ref(null);
const passwordRef = ref(null);
const usernameInvalid = ref(false);
const passwordInvalid = ref(false);
const password = ref('');


const logoUrl = computed(() => {
    return `/layout/images/guimaras-logo.png`;
});

const resetValidation = () => {
        usernameInvalid.value = false
        passwordInvalid.value = false
    }

const login = () => {

    resetValidation()

    if (!username.value || !password.value) {
        if (!username.value || username.value == '') {
            usernameInvalid.value = true
            usernameRef.value.$el.focus()
        } 
        
        if (!password.value || password.value == '') {
            passwordInvalid.value = true
            passwordRef.value.$el.focus()
        }

        return
    }

    axios.post('login', {
        username: username.value,
        password: password.value
    }).then(response => {
        console.log(response)
    }).catch(error => {
        console.log(error)
    })

   

    const resetInput = () => {
        username.value = ''
        password.value = ''
    }
}

</script>

<template>
    <div class="surface-ground flex align-items-center justify-content-center min-h-screen min-w-screen overflow-hidden">
        <div class="flex flex-column align-items-center justify-content-center">
            <img :src="logoUrl" alt="Province of Guimaras Logo" class="mb-5 w-6rem flex-shrink-0 mt-5" />
            <div style="border-radius: 56px; padding: 0.3rem; background: linear-gradient(180deg, var(--primary-color) 10%, rgba(33, 150, 243, 0) 30%)">
                <div class="w-full surface-card py-8 px-5 sm:px-8" style="border-radius: 53px">
                    <div class="text-2xl flex justify-center mb-5">
                        <h1>AICS Treasurer System</h1>
                    </div>
                    <div>
                        <div class="flex flex-col mb-5">
                            <label for="username" class="block text-900 text-xl font-medium mb-2">Username</label>
                            <InputText ref="usernameRef" id="username" type="text" placeholder="Username" class="w-full md:w-30rem" style="padding: 1rem" v-model="username" :invalid="username === ''" />
                            <Tag v-if="usernameInvalid" severity="danger" value="Please input a Username"></Tag>
                        </div>
                        <div class="flex flex-col mb-3">
                            <label for="password1" class="block text-900 font-medium text-xl mb-2">Password</label>
                            <Password ref="passwordRef" id="password1" v-model="password" placeholder="Password" :toggleMask="true" class="w-full" inputClass="w-full" :inputStyle="{ padding: '1rem' }" :invalid="password === ''"></Password>
                            <Tag v-if="passwordInvalid" severity="danger" value="Please input a Password"></Tag>

                        </div>
                        <Button label="Sign In" class="w-full p-3 text-xl bg-sky-700 text-white mt-3" @click="login"></Button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.pi-eye {
    transform: scale(1.6);
    margin-right: 1rem;
}

.pi-eye-slash {
    transform: scale(1.6);
    margin-right: 1rem;
}
</style>
