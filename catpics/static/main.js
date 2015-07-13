var myApp = angular.module('catpics', []).config(function($sceProvider) { $sceProvider.enabled(false); });

myApp.controller('CatPicsController', ['$scope', '$log', '$http', function($scope, $log, $http) {
  function get_picture(){
    $http.get('/api/random').
      success(function(data, status, headers, config) {
        $scope.image= data['image'];
        $scope.type = data['type'];
        $scope.suffix = data['suffix'];
      }).error(function(error) {
        $log.log(error);
      });
  };
  get_picture();
  setInterval(function(){get_picture()}, 30000);
}]);
