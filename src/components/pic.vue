<template>
    <button class = "get_pic" @click = "exportImage()">保存图片</button>
</template>
<script setup name = 'get_pic' lang = 'js'>
    import axios from 'axios';
    import { FieldCenterCard, RushDuelCard, YugiohBackCard, YugiohCard, YugiohSeries2Card } from 'yugioh-card';

    async function exportImage() {
        let cardLeaf = new YugiohCard({
            data: {
                language: 'sc',
                font: '',
                name: '青眼白龙',
                color: '',
                align: 'left',
                gradient: false,
                gradientColor1: '#999999',
                gradientColor2: '#ffffff',
                type: 'monster',
                attribute: 'light',
                icon: '',
                image: './赌上你的灵魂.png',
                cardType: 'normal',
                pendulumType: 'normal-pendulum',
                level: 8,
                rank: 0,
                pendulumScale: 0,
                pendulumDescription: '',
                monsterType: '龙族/通常',
                atkBar: true,
                atk: 3000,
                def: 2500,
                arrowList: [],
                description: '以高攻击力著称的传说之龙。任何对手都能将之粉碎，其破坏力不可估量。',
                firstLineCompress: false,
                descriptionAlign: false,
                descriptionZoom: 1,
                descriptionWeight: 0,
                package: 'SD25-SC001',
                password: '89631139',
                copyright: '',
                laser: '',
                rare: '',
                twentieth: false,
                radius: true,
                scale: 1,
            },
            resourcePath: './yugioh-card',
        });
        let formData = new FormData();
        await cardLeaf.leafer.export('jpg', true).then(result => { 
            formData.append('file', result.data, 'blue-eyes.jpg');
        })
        await axios.post('http://127.0.0.1:8000/api/get_pics', formData)
    }
</script>