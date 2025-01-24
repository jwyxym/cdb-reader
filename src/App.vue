<template>
    <div class = "main_page">
        <div id = "main_page_left">
            <transition name = "slide_list_page">
                <list_page v-if = "show_list_page" @event_close_cdb = "remove_cdb_from_list" @event_select_card = "get_select_card" @event_unshow_list_page = "whether_show_list_page" :cdb = "cdb_menu"/>
            </transition>
            <transition name = "under_list_page">
                <div v-if = "unshow_list_page" id = "under_list_page">
                    <div id = "upload_area" @dragenter.prevent="is_uploading = true" @dragover.prevent="is_uploading = true" @dragleave.prevent="is_uploading = false" @drop.prevent="upload_file" @click="() => { upload_file_input.click(); }">
                        <h4>拖拽文件或点击此处上传文件</h4>
                        <input type = "file" multiple accept="image/*, text/*, .lua, .cdb, .ypk, .zip, .tar, .tgz, .tar.gz, .7z, .rar" ref = "upload_file_input" @change = "click_upload_file" style = "display: none;"/>
                    </div>
                    <div id = "cdb_list">
                        <button v-for="(i, v) in (page > 0? Array(cdbs_list.length >= page * 10? 10 : cdbs_list.length % 10) : [])" :key="v" @click = "whether_show_list_page(v)">{{ cdbs_list[v + (Math.abs(page) - 1) * 10] }}</button>
                    </div>
                    <div class = "cdb_list_btn">
                        <button ref = "prev_btn" @click = "previous_page">上一页</button>
                        <span>第<input @input = "filter_input($event)" v-model = "page"/>页<br>共{{ Math.ceil(cdbs_list.length / 10) }}页</span>
                        <button ref = "next_btn" @click = "next_page">下一页</button>
                    </div>
                </div>
            </transition>
        </div>
        <card_page :cdb = "cdb_menu" :page = "select_page" :card = "select_card" :pic = "upload_new_pic" :close = "close_cdb" @event_close_fixed = "() => { close_cdb = false }"/>
    </div>
</template>

<script setup>
    import list_page from './components/list.vue'
    import card_page from './components/card.vue'

    import { ref, watch, onMounted, computed } from 'vue';
    import axios from 'axios';

    let upload_new_pic = ref('');
    let select_page = ref(0);
    let select_card = ref(0);
    let close_cdb = ref(false);
    let cdb_menu = ref([['暂未打开cdb']]);

    let show_list_page = ref(false);
    let unshow_list_page = ref(true);

    let is_uploading = ref(false);
    let upload_file_input = ref(null);
    let cdbs_list = ref([])
    let opened_cdb_list = ref([])

    let page = ref(0)


    let prev_btn = ref(null);
    let next_btn = ref(null);

    onMounted(() => {
        get_cdbs_list();
        update_button_styles();
    });

    watch(page, () => {
        update_button_styles();
    });

    watch(opened_cdb_list, (new_list) => {
        if (new_list.endsWith('.cdb')) {
            cdbs_list.value.push(new_list);
        }
        if (new_list.endsWith('.jpg')) {
            upload_new_pic.value = new_list;
        }
        if (Math.ceil(cdbs_list.value.length / 10) > page.value) {
            page.value = Math.ceil(cdbs_list.value.length / 10);
        }
    })

    function filter_input(event) {
        let input_value = event.target.value;
        let new_value = input_value.replace(/[^0-9]/, '');
        while (new_value != '' && parseInt(new_value) >= Math.ceil(cdbs_list.value.length / 10))
            new_value = new_value.slice(0, -1);
        if (new_value == '')
            new_value = 0;
        page.value = new_value;
    }

    function get_select_card(get_page, get_card) {
        select_page.value = get_page;
        select_card.value = get_card;
    }

    function next_page() {
        if (page.value < Math.ceil(cdbs_list.value.length / 10)) {
            page.value ++ ;
        }
    }

    function previous_page() {
        if (page.value > 1) {
            page.value -- ;
        }
    }

    function upload_file(e) {
        let files = e.dataTransfer.files;
        if (files.length) {
            for (let i = 0; i < files.length; i++) {
                let file = files[i];
                if (!check_type(file.type, file.name)) {
                    continue;
                }
                let formData = new FormData();
                formData.append('file', file);
                send_file(formData);
            }
        }
        is_uploading.value = false;
    }

    function check_type(type, name) {
        if (type.includes('image') || type.includes('text'))
            return true;
        else if (name.endsWith('.cdb') || name.endsWith('.ypk') || name.endsWith('.zip') || name.endsWith('.tar') || name.endsWith('.tgz') || name.endsWith('.tar.gz') || name.endsWith('.7z') || name.endsWith('.rar') || name.endsWith('.lua'))
            return true;
        
        return false;
    }

    function update_button_styles() {
        btn_style_change(prev_btn.value, 'green', 'white');
        btn_style_change(next_btn.value, 'green', 'white');
        if (page.value <= 1)
            btn_style_change(prev_btn.value, 'gray', 'black');
        if (page.value >= Math.ceil(cdbs_list.value.length / 10))
            btn_style_change(next_btn.value, 'gray', 'black');
    }

    function btn_style_change(btn, btn_color, text_color) {
        if (!btn) return;
        btn.style.backgroundColor = btn_color;
        btn.style.color = text_color;
    }

    async function whether_show_list_page(v = -1) { 
        if (show_list_page.value) {
            show_list_page.value = false;
            await(new Promise(resolve => setTimeout(resolve, 500)));
            unshow_list_page.value = true;
            await(new Promise(resolve => setTimeout(resolve, 5)));
            update_button_styles();
        } else {
            if (v >= 0) {
                get_cdb_menu(v)
            }
            unshow_list_page.value = false;
            await(new Promise(resolve => setTimeout(resolve, 500)));
            show_list_page.value = true;
        }
    }

    async function click_upload_file(e) {
        try {
            let files = e.target.files;
            if (files.length) {
                for (let i = 0; i < files.length; i++) {
                    let file = files[i];
                    let formData = new FormData();
                    formData.append('file', file);
                    send_file(formData);
                }
            }
        } catch (error) {}
    }

    async function get_cdb_menu(v) {
        try {
            let response = await axios.post('http://127.0.0.1:8000/api/get_cdb_menu', {
                cdb: cdbs_list.value[[v + (Math.abs(page.value) - 1) * 10]]
            });
            cdb_menu.value = response.data;
        } catch (error) {}
    }

    async function send_file(formData) {
        try {
            let response = await axios.post('http://127.0.0.1:8000/api/get_file', formData);
            opened_cdb_list.value = response.data;
        } catch (error) {}
    }

    async function remove_cdb_from_list() {
        cdbs_list.value.splice(cdbs_list.value.indexOf(cdb_menu.value[0][0]), 1);
        if (Math.ceil(cdbs_list.value.length / 10) < page.value) {
            page.value = Math.ceil(cdbs_list.value.length / 10);
        }
        try {
            await axios.post('http://127.0.0.1:8000/api/remove_file', {file: cdb_menu.value[0][0]});
        } catch (error) {}
        whether_show_list_page();
        close_cdb.value = true;
    }

    async function get_cdbs_list() {
        try {
            let response = await axios.get('http://127.0.0.1:8000/api/get_cdbs');
            cdbs_list.value = response.data;
            page.value = 1;
        } catch (error) {}
    }
    
    // async function saveFile() {
    //     try {
    //         const opts = {
    //             types: [{
    //                 description: '文件',
    //                 accept: {
    //                     'text/plain': ['.txt'],
    //                     'application/pdf': ['.pdf'],
    //                     'image/jpeg': ['.jpg', '.jpeg'],
    //                     'image/png': ['.png']
    //                 }
    //             }],
    //             excludeAcceptAllOption: true
    //         };

    //         const handle = await window.showSaveFilePicker(opts); // 打开保存文件对话框
    //         const writable = await handle.createWritable(); // 创建可写入的文件对象

    //         // 在这里写入文件内容
    //         await writable.write('这是文件的内容');
    //         await writable.close();

    //         console.log('文件保存成功');
    //         windows.alert('success');
    //     } catch (error) {
    //         console.error('文件保存失败:', error);
    //     }
    // }

</script>

<style scoped>
    .main_page {
        display: flex;
        justify-content: space-between;
    }

    #main_page_left {
        width: 30vw;
        height: 100vh;
    }

    #under_list_page {
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }

    #cdb_list {
        width: 30vw;
        height: 80vh;
    }

    #cdb_list button {
        display: grid;
        align-items:  center;

        width: 30vw;
        height: 8vh;

        border: none;
        border-radius: 4px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);

        cursor: pointer;
    }

    #cdb_list button:hover {
        width: 31vw;
        color: white;
        background-color: green;
    }

    #upload_area {
        width: 25vw;
        height: 10vh;
        border: 2px dashed #bbbbbb;

        color: #bbbbbb;

        text-align: center;
        justify-self: center;

        cursor: pointer;
    }

    #upload_area:hover {
        border: 2px dashed black;
        color: black;
    }

    .cdb_list_btn {
        display: flex;
        align-items:  center;
    }

    .cdb_list_btn button {
        width: 10vw;
        height: 8vh;
        border: none;
        border-radius: 4px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);

        cursor: pointer;
    }

    .cdb_list_btn span {
        width: 10vw;
        height: 8vh;
        text-align: center;
    }

    .cdb_list_btn input {
        width: 3vw;
    }

    .slide_list_page-enter-active,
    .slide_list_page-leave-active {
        transition: transform 0.5s ease;
    }

    .slide_list_page-enter-from,
    .slide_list_page-leave-to {
        transform: translateX(-100%);
    }

    .slide_list_page-enter-to,
    .slide_list_page-leave-from {
        transform: translateX(0%);
    }

    .under_list_page-enter-active,
    .under_list_page-leave-active {
        transition: transform 0.5s ease;
    }

    .under_list_page-enter-from,
    .under_list_page-leave-to {
        transform: translateX(-100%);
    }

    .under_list_page-enter-to,
    .under_list_page-leave-from {
        transform: translateX(0%);
    }
</style>