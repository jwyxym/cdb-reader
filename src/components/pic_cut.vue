<template>
    <div class = "pic_cut">
        <img ref = "image" :src = "card.url">
        <div>
            <el-button
                @click = "emit.card_page.upload.to('confirm')"
                v-if = "card.url != ''"
            >
                <el-icon><Check/></el-icon>
                <span>确认</span>
            </el-button>
            <el-button
                @click = "emit.card_page.upload.to('cancel')"
                v-if = "card.url != ''"
            >
                <el-icon><Close/></el-icon>
                <span>取消</span>
            </el-button>
        </div>
    </div>
</template>
  
<script setup name = "pic_cut" lang = "ts">
    import { ref, reactive, onMounted, onBeforeUnmount } from 'vue';
    import Cropper from 'cropperjs';
    import 'cropperjs/dist/cropper.css';
    import emitter from '@/utils/emitter';
  
    let image = ref(null);

    let card = reactive({
        url : '',
        id : 0
    });

    let pic : Cropper;

    let cropper = reactive({
        init : function() {
            pic = new Cropper(image.value, {
                aspectRatio: 1,
                viewMode: 2,
                crop(event) {},
            });
        }
    });

    let emit = {
        card_page : {
            upload : {
                on : function() {
                    emitter.on('to_pcpage_upload', async (i : Map<string, any>) => {
                        if (pic) {
                            pic.destroy();
                            URL.revokeObjectURL(card.url);
                        }
                        card.url = i.get('url');
                        card.id = i.get('id');
                        await (new Promise(resolve => setTimeout(resolve, 2)));
                        cropper.init();
                    });
                } as () => void,
                to : function(str) {
                    if (str == 'confirm')
                        pic.getCroppedCanvas().toBlob(function (blob) {
                            let file = new File([blob], `${card.id}.jpg`, { type: 'image/jpeg' });
                            emitter.emit('to_cpage_upload', file);
                            card.url = '';
                            card.id = 0;
                            pic.destroy();
                        }, 'image/jpeg');
                    else if (str == 'cancel') {
                        URL.revokeObjectURL(card.url);
                        card.url = '';
                        card.id = 0;
                        pic.destroy();
                    }
                } as (str: string) => void
            }
        }
    }

    emit.card_page.upload.on();
</script>
  
<style scoped>
    .pic_cut {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        grid-template-rows: repeat(3, 1fr);

        justify-items: center;
        align-items: center;

        height: 80%;
        width: 100%;
    }

    .pic_cut div {
        grid-column-start: 1;
        grid-column-end: 3;
        grid-row-start: 3;
        grid-row-end: 4;

        display: flex;
        justify-items: center;
        align-items: center;
    }

    img {
        display: block;
        max-width: 100%;
        max-height: 100%;

        grid-column-start: 1;
        grid-column-end: 3;
        grid-row-start: 1;
        grid-row-end: 3;
    }
</style>
  