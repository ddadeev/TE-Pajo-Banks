import React, { useState } from 'react';
import { Upload, Camera, ImagePlus } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';

const CardRecognitionApp = () => {
  const [inputMethod, setInputMethod] = useState('upload');
  const [selectedImage, setSelectedImage] = useState(null);
  const [predictions, setPredictions] = useState(null);

  const cardSuits = ['♠', '♥', '♦', '♣'];
  const cardColors = {
    '♠': 'text-black',
    '♥': 'text-red-600',
    '♦': 'text-red-600',
    '♣': 'text-black'
  };

  const mockPredictions = [
    { name: 'Ace of Spades', probability: 0.85 },
    { name: 'King of Spades', probability: 0.10 },
    { name: 'Queen of Spades', probability: 0.05 }
  ];

  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setSelectedImage(reader.result);
        // Simulate prediction (in real app, this would be an API call)
        setPredictions(mockPredictions);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleCameraCapture = (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setSelectedImage(reader.result);
        // Simulate prediction (in real app, this would be an API call)
        setPredictions(mockPredictions);
      };
      reader.readAsDataURL(file);
    }
  };

  const renderPredictionCard = (prediction) => {
    // Extract suit from the card name
    const suit = cardSuits.find(s => prediction.name.includes(s.toLowerCase())) || '♠';
    const suitColor = cardColors[suit];

    return (
      <Card key={prediction.name} className="mb-2 shadow-sm">
        <CardHeader className="pb-2">
          <CardTitle className={`text-lg ${suitColor}`}>
            {prediction.name}
          </CardTitle>
        </CardHeader>
        <CardContent>
          <Progress 
            value={prediction.probability * 100} 
            className="w-full h-2 bg-gray-200"
          />
          <p className="text-sm text-gray-600 mt-2">
            Confidence: {(prediction.probability * 100).toFixed(1)}%
          </p>
        </CardContent>
      </Card>
    );
  };

  return (
    <div className="max-w-md mx-auto p-4 bg-white rounded-xl shadow-2xl">
      <h1 className="text-3xl font-bold mb-6 text-center text-gray-800">
        Card Recognition
      </h1>

      {/* Input Method Selector */}
      <div className="flex justify-center mb-6 bg-gray-100 rounded-full p-1">
        <Button 
          variant={inputMethod === 'upload' ? 'default' : 'ghost'}
          onClick={() => setInputMethod('upload')}
          className="rounded-full mr-2"
        >
          <Upload className="mr-2" /> Upload
        </Button>
        <Button 
          variant={inputMethod === 'camera' ? 'default' : 'ghost'}
          onClick={() => setInputMethod('camera')}
          className="rounded-full"
        >
          <Camera className="mr-2" /> Camera
        </Button>
      </div>

      {/* Image Upload/Capture Section */}
      <Card className="mb-6">
        <CardContent className="p-4 text-center">
          {!selectedImage ? (
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-6">
              <ImagePlus className="mx-auto mb-4 text-gray-400" size={48} />
              <p className="text-gray-600">
                {inputMethod === 'upload' 
                  ? 'Select an image to upload' 
                  : 'Capture an image with your camera'}
              </p>
              <input 
                type="file" 
                accept="image/*" 
                capture={inputMethod === 'camera' ? 'environment' : undefined}
                onChange={inputMethod === 'upload' ? handleImageUpload : handleCameraCapture}
                className="hidden"
                id="imageInput"
              />
              <label 
                htmlFor="imageInput" 
                className="mt-4 inline-block bg-blue-500 text-white px-4 py-2 rounded-lg cursor-pointer hover:bg-blue-600"
              >
                Choose File
              </label>
            </div>
          ) : (
            <div>
              <img 
                src={selectedImage} 
                alt="Selected" 
                className="max-h-64 mx-auto rounded-lg object-contain"
              />
            </div>
          )}
        </CardContent>
      </Card>

      {/* Prediction Results */}
      {predictions && (
        <div>
          <h2 className="text-xl font-semibold mb-4 text-center">
            Prediction Results
          </h2>
          {predictions.map(renderPredictionCard)}
        </div>
      )}
    </div>
  );
};

export default CardRecognitionApp;
