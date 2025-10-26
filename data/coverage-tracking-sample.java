public static void fuzzerTestOneInput(FuzzedDataProvider data) {
   RT.getAgent().setRecording(false);

   // Parameter/ Instance preparation
   Options o = prepareOptions(data);

   try{
      RT.getAgent().setRecording(true);
      Parser.parse(o);
      RT.getAgent().setRecording(false);
   } catch (IllegalArgumentException var15) {
      }
}