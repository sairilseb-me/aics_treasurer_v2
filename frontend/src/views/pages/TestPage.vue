<template>
    <div>
        <div className="card">
        <h5>This is a test Page</h5>
        <p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Veritatis nostrum impedit neque. Quam, laudantium facere eaque nisi necessitatibus placeat cupiditate assumenda tempore hic, itaque quo, iure exercitationem velit fuga sed.
        Commodi repellendus esse provident corrupti nesciunt repudiandae ducimus sequi rerum facere ipsa! Corrupti, commodi, dolore deleniti illum officiis voluptas eum corporis numquam, itaque maxime magni ut earum provident sint deserunt!
        Ratione quae vero necessitatibus culpa dolorem assumenda aliquid! Maiores quia illo cupiditate debitis quidem error nemo rerum cumque perferendis. Aperiam itaque modi consequuntur necessitatibus aut minus hic eum blanditiis ad!
        Sint perferendis, odit voluptatem possimus qui atque voluptatibus voluptatum nihil quos harum tempora minima, iure iusto, odio labore libero! Et commodi expedita possimus enim veritatis iste quaerat vel delectus odit?
        Unde rerum optio, itaque exercitationem expedita facilis magnam saepe deleniti necessitatibus delectus odit a ipsum veritatis vel. Temporibus doloribus est corporis. Obcaecati blanditiis eum consectetur reiciendis iste deserunt saepe libero?</p>
        </div>
        <Button class="border border-solid border-slate-700 bg-blue-700 text-white py-2 px-5"  @click="showSuccess">Test Toast</Button>
    </div>
   
</template>

<script>

import {ref} from 'vue'
import  Button from 'primevue/button'
import  ToastService from '@/plugins/toasts'
export default {
    components: {
        Button,
    },
    setup() {
        const visible = ref(false)
        
        const toast = new ToastService()

        const showSuccess = () => {
            toast.showMessage('success', 'Success Message', 'This is a success message')
        }
      
        return {
          
            showSuccess,
        }
    },
}
</script>
