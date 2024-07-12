import { useToast } from "primevue/usetoast";


class ToastService  {
    toast = useToast();

    showMessage = (status, summary, message) => {
        this.toast.add({ severity: status, summary: summary, detail: message, life: 5000 });
    }
}

export default ToastService;

