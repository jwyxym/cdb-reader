<template>
    <img class = "pic" :src = "url_blob" />
</template>
<script setup name = 'pic' lang = 'js'>
    import { ref, reactive, watch, onMounted, computed } from 'vue';
    import axios from 'axios';
    import emitter from '@/utils/emitter';
    import { FieldCenterCard, RushDuelCard, YugiohBackCard, YugiohCard, YugiohSeries2Card } from 'yugioh-card';
    onMounted(() => {
        exportImage();
    })

    let url_blob = ref(null);

    function to_data (card, card_n) {
        if(!card || !card_n) return;
        let data = {
            language: 'sc',
            font: '',
            name: card.name,
            color: '',
            align: 'left',
            gradient: false,
            gradientColor1: '#999999',
            gradientColor2: '#ffffff',
            type: 'monster',
            attribute: '',
            icon: '',
            image: './赌上你的灵魂.png',  // to be continued
            cardType: 'normal',
            pendulumType: 'normal-pendulum',
            level: card_n.level & 0xffff,
            rank: card_n.level & 0xffff,
            pendulumScale: card.pendulum,
            pendulumDescription: '', // to be continued
            monsterType: '', // to be continued
            atkBar: true,
            atk: card_n.atk >= 0 ? card_n.atk : -1,
            def: card_n.def >= 0 ? card_n.def : -1,
            arrowList: [],
            description: card.desc,
            firstLineCompress: false,
            descriptionAlign: false,
            descriptionZoom: 1,
            descriptionWeight: 0,
            package: '',
            password: card_n.id,
            copyright: '',
            laser: '',
            rare: '',
            twentieth: false,
            radius: true,
            scale: 1,
        }

        let list = {
            type : new Map ([
                [0x1,'monster'],
                [0x2,'spell'],
                [0x4, 'trap'],
                [0x1000000, 'pendulum']
            ]),
            monster_type : new Map ([
                [0x1, 'normal'],
                [0x20, 'effect'],
                [0x40, 'fusion'],
                [0x80, 'ritual'],
                [0x2000, 'synchro'],
                [0x4000, 'token'],
                [0x800000, 'xyz'],
                [0x4000000, 'link']
            ]),
            p_type : new Map ([
                [0x1, 'normal-pendulum'],
                [0x20, 'effect-pendulum'],
                [0x40, 'fusion-pendulum'],
                [0x80, 'ritual-pendulum'],
                [0x2000,'synchro-pendulum'],
                [0x800000, 'xyz-pendulum']
            ]),
            link : new Map ([
                [0x1, 6],
                [0x2, 5],
                [0x4, 4],
                [0x8, 7],
                [0x20, 3],
                [0x40, 8],
                [0x80, 1],
                [0x100, 2]
            ]),
            spell_type : new Map ([
                [0x80, 'ritual'],
                [0x10000, 'quick-play'],
                [0x20000, 'continuous'],
                [0x40000, 'equip'],
                [0x80000, 'field']
            ]),
            trap_type : new Map ([
                [0x20000, 'continuous'],
                [0x100000, 'counter']
            ]),
            attribute : new Map ([
                [0x1, 'earth'],
                [0x2, 'water'],
                [0x4, 'fire'],
                [0x8, 'wind'],
                [0x10, 'light'],
                [0x20, 'dark'],
                [0x40, 'divine']
            ]),
        }
        list.type.forEach((value, key) => {
            if((card_n.type & key) > 0)
                data.type = value;
        });

        switch(data.type){
            case'monster' :
                list.attribute.forEach((value, key) => {
                    if((card_n.attribute & key) > 0)
                        data.attribute = value;
                });
                list.monster_type.forEach((value, key) => {
                    if((card_n.type & key) > 0)
                        data.cardType = value;
                    });
                if (data.cardType == 'link')
                    list.link.forEach((value, key) => {
                        if((card_n.def & key) > 0)
                            data.arrowList.push(value);
                    });
                break;
            case 'spell' :
                list.spell_type.forEach((value, key) => {
                    if((card_n.type & key) > 0)
                        data.icon = value;
                });
                break;
            case 'trap' :
                list.trap_type.forEach((value, key) => {
                    if((card_n.type & key) > 0)
                        data.icon = value;
                });
                break;
            case 'pendulum' :
                list.p_type.forEach((value, key) => {
                    if((card_n.type & key) > 0) {
                        data.pendulumType = value;
                    }
                });
                break;
        }

        return data;
    }

    async function exportImage(card, card_n) {
        let cardLeaf = new YugiohCard({
            data: to_data (card, card_n),
            resourcePath: './yugioh-card',
        });
        let formData = new FormData();
        await cardLeaf.leafer.export('jpg', true).then(result => { 
            formData.append('file', result.data, 'blue-eyes.jpg');
            if (url_blob.value)
                URL.revokeObjectURL(url_blob.value);
            url_blob.value = URL.createObjectURL(result.data);
        })
        await axios.post('http://127.0.0.1:8000/api/get_pics', formData)
    }
    emitter.on('exportImage', (obj)=>{
        exportImage(obj.data1, obj.data2);
    });
</script>