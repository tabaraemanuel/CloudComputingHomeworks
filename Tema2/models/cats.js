const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const catsSchema = new Schema({
    name: {
        type: String,
        unique: true,
        required: true
    },
    owner: {
        type: String,
        required: true
    }
}, {timestamps: true});

const Cat = mongoose.model('cat', catsSchema);
module.exports = Cat;