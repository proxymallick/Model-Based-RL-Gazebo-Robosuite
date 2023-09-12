
"use strict";

let GetLoadedProgram = require('./GetLoadedProgram.js')
let GetRobotMode = require('./GetRobotMode.js')
let GetSafetyMode = require('./GetSafetyMode.js')
let Load = require('./Load.js')
let RawRequest = require('./RawRequest.js')
let GetProgramState = require('./GetProgramState.js')
let IsProgramSaved = require('./IsProgramSaved.js')
let IsProgramRunning = require('./IsProgramRunning.js')
let Popup = require('./Popup.js')
let AddToLog = require('./AddToLog.js')

module.exports = {
  GetLoadedProgram: GetLoadedProgram,
  GetRobotMode: GetRobotMode,
  GetSafetyMode: GetSafetyMode,
  Load: Load,
  RawRequest: RawRequest,
  GetProgramState: GetProgramState,
  IsProgramSaved: IsProgramSaved,
  IsProgramRunning: IsProgramRunning,
  Popup: Popup,
  AddToLog: AddToLog,
};
