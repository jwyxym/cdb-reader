<template>
    <img class = "pic" :src = "url_blob" />
</template>
<script setup name = 'pic' lang = 'js'>
    import { ref, reactive, watch, onMounted, computed } from 'vue';
    import axios from 'axios';
    import emitter from '@/utils/emitter';
    import { FieldCenterCard, RushDuelCard, YugiohBackCard, YugiohCard, YugiohSeries2Card } from 'yugioh-card';
    
    let url_blob = ref(null);

    function to_data (card, card_n, type_list, pic) {
        if(!card || !card_n || !type_list || !pic) return;
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
            image: card.center_pic,
            cardType: 'normal',
            pendulumType: 'normal-pendulum',
            level: card_n.level & 0xffff,
            rank: card_n.level & 0xffff,
            pendulumScale: card.pendulum,
            pendulumDescription: '',
            monsterType: card.race != '种族 N/A' ? `${card.race}族` : '',
            atkBar: true,
            atk: card_n.atk >= 0 ? card_n.atk : -1,
            def: card_n.def >= 0 ? card_n.def : -1,
            arrowList: [],
            description: card.desc,
            firstLineCompress: pic.firstLineCompress,
            descriptionAlign: pic.descriptionAlign,
            descriptionZoom: pic.descriptionZoom,
            descriptionWeight: pic.descriptionWeight,
            package: pic.package,
            password: card_n.id,
            copyright: pic.copyright,
            laser: pic.laser,
            rare: pic.rare,
            twentieth: false,
            radius: pic.radius,
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
                if (card.desc.includes('【怪兽效果】') && card.desc.includes(`←${card.pendulum} 【灵摆】 ${card.pendulum}→`)) {
                    data.pendulumDescription = card.desc.split(`←${card.pendulum} 【灵摆】 ${card.pendulum}→`)[1].split('【怪兽效果】')[0].replace(/\s*[\r\n]/, '');
                    data.description = card.desc.split('【怪兽效果】')[1].replace(/\s*[\r\n]/, '');
                }
                break;
        }

        if (card.desc.includes('【怪兽效果】') && card.desc.includes(`←${card.pendulum} 【灵摆】 ${card.pendulum}→`)) {
            data.pendulumDescription = card.desc.split(`←${card.pendulum} 【灵摆】 ${card.pendulum}→`)[1].split('【怪兽效果】')[0].replace(/\s*[\r\n]/, '');
            data.description = card.desc.split('【怪兽效果】')[1].replace(/\s*[\r\n]/, '');
        }

        type_list = type_list.filter(item => ![0x1, 0x40, 0x80, 0x2000, 0x800000, 0x2000000].includes(item[0]));
        type_list.sort((a, b) => b[0] - a[0]);
        type_list.splice(type_list.findIndex(e => e.includes(0x1000000)), 0, [0x40, '融合'], [0x80, '仪式'], [0x2000, '同调'], [0x800000, '超量'], [0x2000000, '特殊召唤']);
        for (let i = 0; i < type_list.length; i++) {
            if ((card_n.type & type_list[i][0]) > 0)
                data.monsterType += `${data.monsterType == '' ? '' : '/'}${type_list[i][1]}`
        }

        if (data.cardType == 'fusion' || data.cardType == 'synchro' || data.cardType == 'xyz' || data.cardType == 'link') {
            let i = data.description.split(/\s*[\r\n]/)
            data.description = `${i[0]}\r\n${data.description.replace(i[0], '').replace(/\s*[\r\n]/g, '')}`;
        } else {
            data.description = data.description.replace(/\s*[\r\n]/g, '');
        }
        return data;
    }

    async function exportImage(chk, card, card_n, type_list, pic, open) {
        let cardLeaf = new YugiohBackCard({
            data: {
                type: 'normal',
                logo: '',
                konami: false,
                register: false,
                radius: pic.radius,
                scale: 1,
            },
            resourcePath: './yugioh-card',
        });
        if (open != '')
            cardLeaf = new YugiohCard({
                data: to_data (card, card_n, type_list, pic),
                resourcePath: './yugioh-card',
            });
        if (chk == 'load') {
            await cardLeaf.leafer.export('jpg', true).then(result => { 
                if (url_blob.value)
                    URL.revokeObjectURL(url_blob.value);
                url_blob.value = URL.createObjectURL(result.data);
            });
        } else if (chk == 'download' && open != '' && card.center_pic != '' && card_n.id > 0) {
            let formData = new FormData();
                await cardLeaf.leafer.export('jpg', true).then(result => { 
                formData.append('file', result.data, `${card_n.id}.jpg`);
            });
            await axios.post(`${window.location.href}api/get_pics`, formData);
        }
    }
    emitter.on('to_ppage_unload_pic', ()=>{
        if (url_blob.value)
            URL.revokeObjectURL(url_blob.value);
        url_blob.value = null;
    });
    emitter.on('to_ppage_load_pic', (i)=>{
        exportImage('load', i.get('card'), i.get('card_n'), i.get('list'), i.get('pic'), i.get('open'));
    });
    emitter.on('to_ppage_download_pic', (i)=>{
        exportImage('download', i.get('card'), i.get('card_n'), i.get('list'), i.get('pic'), i.get('open'));
    });
</script>